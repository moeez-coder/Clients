"""Shared definitions for the GRN Piedmont data-source review (2026-11-24).

The "same ICP slice" every source is run against:
  MFG slice : US manufacturers, HQ in North Carolina or South Carolina, 201-1,000 employees.
              (GRN's home region; small enough to pull in full from each source so overlap is exact.)
  FLS slice : US fire & life safety companies (sprinkler/suppression, alarm/detection, ITM),
              HQ in an Eastern or Central time-zone state, 201-1,000 employees.
Labels reuse ../tam/tam_counts.py (2026-11-16 TAM read) so this review and the TAM read agree.
"""
import json, os, re, sys, time, urllib.request, urllib.error
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tam"))
from tam_counts import MFG, FLS_IND, FLS_KW, NON_ET_CT, SIZES  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MFG_STATES = ["North Carolina", "South Carolina"]
ET_CT_STATES = ["Alabama", "Arkansas", "Connecticut", "Delaware", "Florida", "Georgia", "Illinois", "Indiana", "Iowa",
                "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
                "Mississippi", "Missouri", "Nebraska", "New Hampshire", "New Jersey", "New York", "North Carolina",
                "North Dakota", "Ohio", "Oklahoma", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
                "Tennessee", "Texas", "Vermont", "Virginia", "West Virginia", "Wisconsin", "District of Columbia"]
UA = "curl/8.5.0"


def http(method, url, headers=None, body=None, timeout=90, tries=5):
    h = {"User-Agent": UA, "Content-Type": "application/json"}
    h.update(headers or {})
    data = json.dumps(body).encode() if body is not None else None
    for a in range(tries):
        try:
            r = urllib.request.Request(url, data, h, method=method)
            with urllib.request.urlopen(r, timeout=timeout) as resp:
                return resp.status, json.loads(resp.read() or b"null")
        except urllib.error.HTTPError as e:
            txt = e.read()[:2000].decode(errors="replace")
            if e.code in (429, 500, 502, 503, 504) and a < tries - 1:
                time.sleep(2 ** a); continue
            return e.code, {"_error": txt}
        except Exception as e:  # network
            if a < tries - 1: time.sleep(2 ** a); continue
            return 0, {"_error": str(e)}


def norm_domain(d):
    if not d or d == "-": return ""
    d = d.strip().lower()
    d = re.sub(r"^https?://", "", d); d = re.sub(r"^www\.", "", d)
    return d.split("/")[0].split("?")[0]


def norm_li(u):
    """Company LinkedIn URL -> 'linkedin.com/company/<slug>' (lowercase), '' if none."""
    if not u or u == "-": return ""
    u = u.strip().lower()
    m = re.search(r"linkedin\.com/(company|school|showcase)/([^/?#]+)", u)
    return f"linkedin.com/company/{m.group(2)}" if m else ""
