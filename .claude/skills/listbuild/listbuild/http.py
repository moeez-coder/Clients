"""Small HTTP wrapper: shared rate limit, retries with backoff for 429/5xx, JSON in/out."""
import random
import threading
import time

import requests


class RateLimiter:
    """Token bucket shared across threads. rps=None disables limiting."""

    def __init__(self, rps):
        self.rps = rps
        self.lock = threading.Lock()
        self.next_slot = time.monotonic()

    def wait(self):
        if not self.rps:
            return
        with self.lock:
            now = time.monotonic()
            slot = max(self.next_slot, now)
            self.next_slot = slot + 1.0 / self.rps
        delay = slot - time.monotonic()
        if delay > 0:
            time.sleep(delay)


class HttpError(Exception):
    def __init__(self, status, body, url):
        super().__init__(f"HTTP {status} from {url}: {str(body)[:300]}")
        self.status = status
        self.body = body


class Http:
    def __init__(self, base_url, headers, rps=None, max_retries=5, timeout=90, retry_timeouts=True):
        self.base_url = base_url.rstrip("/")
        self.headers = headers
        self.limiter = RateLimiter(rps)
        self.max_retries = max_retries
        self.timeout = timeout
        self.retry_timeouts = retry_timeouts
        self.session = requests.Session()
        self.calls = 0
        self.retries = 0

    def request(self, method, path, params=None, json=None):
        url = self.base_url + path if path.startswith("/") else path
        attempt = 0
        while True:
            self.limiter.wait()
            self.calls += 1
            try:
                r = self.session.request(method, url, headers=self.headers, params=params, json=json, timeout=self.timeout)
            except (requests.Timeout, requests.ConnectionError) as e:
                if not self.retry_timeouts or attempt >= self.max_retries:
                    raise
                attempt += 1
                self.retries += 1
                time.sleep(min(30, 2 ** attempt) + random.random())
                continue
            if r.status_code in (429,) or r.status_code >= 500:
                if attempt >= self.max_retries:
                    raise HttpError(r.status_code, r.text, url)
                attempt += 1
                self.retries += 1
                retry_after = r.headers.get("Retry-After")
                try:
                    delay = float(retry_after) if retry_after else min(60, 2 ** attempt)
                except ValueError:
                    delay = min(60, 2 ** attempt)
                time.sleep(delay + random.random())
                continue
            if r.status_code >= 400:
                raise HttpError(r.status_code, r.text, url)
            if not r.content:
                return {}
            try:
                return r.json()
            except ValueError:
                return {"_raw": r.text}
