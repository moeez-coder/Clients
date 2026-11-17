"""Glassdoor company lookup (We Are DNA), full run 2026-11-17: call Apify actor kaix/glassdoor-company-scraper
directly over the Apify API for a slice of the stage-2 lookup input, wait, download the dataset, and log the
run's id, status and real cost. Stdlib only; run with `python -I run_lookup.py ...`.

Token: read from env APIFY_API_TOKEN or Apify_API_KEY (this environment's name); never printed.

Usage:
  run_lookup.py run  --batch N [--start I] [--end J] --cap USD [--timeout SECS]
      Runs input rows of batch N, positions [I, J) within the batch (input-file order, largest first).
      --cap sets Apify's maxTotalChargeUsd for the run (the hard per-run spend limit).
      Items go to <scratch>/runs/<run_id>.jsonl; the run is appended to RUNLOG.
  run_lookup.py assemble --batch N
      Writes 2026-11-17-glassdoor-profiles-raw-bN.jsonl.gz from every logged run of batch N (append-only:
      refuses to overwrite an existing file unless --force).
  run_lookup.py spent
      Prints the summed real cost (usageTotalUsd) of every logged run.

Actor input (Moe's approved settings, same as Preview 2):
  searchQueries = `search_query` column, maxSearchResults 3, compactMode false, includeRatings true,
  every other include* false, maxPhotos 0.
"""
import argparse, csv, gzip, json, os, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(HERE, "2026-11-17-glassdoor-lookup-input.csv")
RUNLOG = os.path.join(HERE, "2026-11-17-glassdoor-lookup-runs.json")
RAW_FMT = os.path.join(HERE, "2026-11-17-glassdoor-profiles-raw-b{}.jsonl.gz")
SCRATCH = os.environ.get("LOOKUP_SCRATCH", os.path.join(HERE, ".scratch"))
ACTOR = "kaix~glassdoor-company-scraper"
API = "https://api.apify.com/v2"
TOTAL_CAP_USD = 10.0   # Moe's hard cap across all runs

ACTOR_INPUT = {
    "maxSearchResults": 3, "compactMode": False, "includeRatings": True,
    "includeDemographics": False, "includeReviewLocations": False, "includeOfficeLocations": False,
    "includeManagedContent": False, "includeCompanyUpdates": False, "includePhotos": False,
    "includeSalaries": False, "includeBenefits": False, "includeInterviews": False, "includeJobs": False,
    "maxPhotos": 0,
}


def token():
    t = os.environ.get("APIFY_API_TOKEN") or os.environ.get("Apify_API_KEY")
    if not t:
        sys.exit("no Apify token in env (APIFY_API_TOKEN / Apify_API_KEY)")
    return t


def call(method, path, body=None, raw=False):
    req = urllib.request.Request(API + path, method=method,
                                 data=None if body is None else json.dumps(body).encode(),
                                 headers={"Authorization": "Bearer " + token(), "Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
                return data if raw else json.loads(data)
        except (urllib.error.URLError, TimeoutError) as e:
            if isinstance(e, urllib.error.HTTPError) and e.code < 500 and e.code != 429:
                sys.exit(f"{method} {path.split('?')[0]} -> HTTP {e.code}: {e.read()[:300]!r}")
            time.sleep(5 * (attempt + 1))
    sys.exit(f"{method} {path.split('?')[0]} failed after retries")


def load_log():
    return json.load(open(RUNLOG)) if os.path.exists(RUNLOG) else []


def save_log(log):
    with open(RUNLOG, "w") as f:
        json.dump(log, f, indent=1)
        f.write("\n")


def batch_rows(n):
    return [r for r in csv.DictReader(open(INPUT, newline="", encoding="utf-8")) if r["batch"] == str(n)]


def cmd_run(a):
    rows = batch_rows(a.batch)
    end = len(rows) if a.end is None else min(a.end, len(rows))
    sl = rows[a.start:end]
    queries = [r["search_query"] for r in sl]
    if not queries:
        sys.exit("empty slice")
    log = load_log()
    committed = sum(e["cap_usd"] for e in log if e.get("cost_usd") is None) + sum(e["cost_usd"] or 0 for e in log)
    if committed + a.cap > TOTAL_CAP_USD + 1e-9:
        sys.exit(f"cap check: spent/committed ${committed:.2f} + this cap ${a.cap:.2f} > ${TOTAL_CAP_USD:.2f}")

    body = dict(ACTOR_INPUT, searchQueries=queries)
    q = f"?maxTotalChargeUsd={a.cap}&timeout={a.timeout}&memory={a.memory}"
    run = call("POST", f"/acts/{ACTOR}/runs{q}", body)["data"]
    rid = run["id"]
    entry = {"run_id": rid, "batch": a.batch, "start": a.start, "end": end, "queries": len(queries),
             "cap_usd": a.cap, "started_at": run["startedAt"], "status": run["status"],
             "dataset_id": run["defaultDatasetId"], "items": None, "cost_usd": None, "charged_events": None}
    log.append(entry)
    save_log(log)
    print(f"run {rid} started: batch {a.batch} rows [{a.start},{end}) = {len(queries)} queries, cap ${a.cap}")

    while True:
        time.sleep(20)
        run = call("GET", f"/actor-runs/{rid}")["data"]
        st = run["status"]
        print(f"  {time.strftime('%H:%M:%S')} {st} items~{(run.get('chargedEventCounts') or {}).get('apify-default-dataset-item')}"
              f" usd={run.get('usageTotalUsd')}", flush=True)
        if st not in ("READY", "RUNNING"):
            break

    os.makedirs(os.path.join(SCRATCH, "runs"), exist_ok=True)
    out = os.path.join(SCRATCH, "runs", rid + ".jsonl")
    n, off = 0, 0
    with open(out, "w", encoding="utf-8") as f:
        while True:
            items = call("GET", f"/datasets/{run['defaultDatasetId']}/items?format=json&clean=1&offset={off}&limit=1000")
            for it in items:
                f.write(json.dumps(it, ensure_ascii=False) + "\n")
            n += len(items)
            off += len(items)
            if len(items) < 1000:
                break
    entry.update(status=run["status"], finished_at=run.get("finishedAt"), items=n,
                 cost_usd=run.get("usageTotalUsd"), charged_events=run.get("chargedEventCounts"),
                 status_message=run.get("statusMessage"))
    save_log(log)
    print(f"run {rid} {run['status']}: {n} items, cost ${run.get('usageTotalUsd')}, events {run.get('chargedEventCounts')}")
    print(f"total real spend so far: ${sum(e['cost_usd'] or 0 for e in log):.4f}")


def cmd_runall(a):
    """Launch every not-yet-logged chunk of `--chunk` queries for the given batches, at most `--parallel` at
    once. Per-run cap = chunk x maxSearchResults x price + start fee, so a cap can never cut a run short; the
    sum of all caps plus spend so far must stay under TOTAL_CAP_USD or nothing starts."""
    import threading
    log = load_log()
    plan = []
    for b in a.batches:
        n = len(batch_rows(b))
        ok = [(e["start"], e["end"]) for e in log if e["batch"] == b and e["status"] == "SUCCEEDED"]
        cuts = sorted({*range(0, n, a.chunk), n} | {x for se in ok for x in se})
        for s, e_ in zip(cuts, cuts[1:]):
            if not any(os_ <= s and e_ <= oe for os_, oe in ok):   # skip ranges a successful run already covers
                plan.append((b, s, e_))
    spent = sum(e["cost_usd"] or 0 for e in log)
    need = spent + a.cap * len(plan)
    print(f"{len(plan)} runs planned; spent ${spent:.4f}; caps ${a.cap * len(plan):.2f}; worst case ${need:.2f}")
    if need > TOTAL_CAP_USD + 1e-9:
        sys.exit("would exceed the $10 total cap; nothing started")
    if a.dry:
        for x in plan: print(" ", x)
        return
    lock, sem = threading.Lock(), threading.Semaphore(a.parallel)

    def one(b, s, e_):
        with sem:
            rows = batch_rows(b)[s:e_]
            body = dict(ACTOR_INPUT, searchQueries=[r["search_query"] for r in rows])
            run = call("POST", f"/acts/{ACTOR}/runs?maxTotalChargeUsd={a.cap}&timeout={a.timeout}&memory=512", body)["data"]
            rid = run["id"]
            entry = {"run_id": rid, "batch": b, "start": s, "end": e_, "queries": len(rows), "cap_usd": a.cap,
                     "started_at": run["startedAt"], "status": run["status"], "dataset_id": run["defaultDatasetId"],
                     "items": None, "cost_usd": None, "charged_events": None}
            with lock:
                lg = load_log(); lg.append(entry); save_log(lg)
            while run["status"] in ("READY", "RUNNING"):
                time.sleep(60)
                run = call("GET", f"/actor-runs/{rid}")["data"]
            os.makedirs(os.path.join(SCRATCH, "runs"), exist_ok=True)
            n, off = 0, 0
            with open(os.path.join(SCRATCH, "runs", rid + ".jsonl"), "w", encoding="utf-8") as f:
                while True:
                    items = call("GET", f"/datasets/{run['defaultDatasetId']}/items?format=json&clean=1&offset={off}&limit=1000")
                    for it in items:
                        f.write(json.dumps(it, ensure_ascii=False) + "\n")
                    n += len(items); off += len(items)
                    if len(items) < 1000:
                        break
            with lock:
                lg = load_log()
                for x in lg:
                    if x["run_id"] == rid:
                        x.update(status=run["status"], finished_at=run.get("finishedAt"), items=n,
                                 cost_usd=run.get("usageTotalUsd"), charged_events=run.get("chargedEventCounts"),
                                 status_message=run.get("statusMessage"))
                save_log(lg)
                print(f"{time.strftime('%H:%M:%S')} b{b} [{s},{e_}) {rid} {run['status']} items={n} "
                      f"${run.get('usageTotalUsd')}  total ${sum(x['cost_usd'] or 0 for x in lg):.4f}", flush=True)

    ts = [threading.Thread(target=one, args=p) for p in plan]
    for t in ts:
        t.start(); time.sleep(1)
    for t in ts:
        t.join()


def cmd_assemble(a):
    out = RAW_FMT.format(a.batch)
    if os.path.exists(out) and not a.force:
        sys.exit(f"{os.path.basename(out)} exists (append-only); use --force only to rebuild from the same runs")
    runs = [e for e in load_log() if e["batch"] == a.batch and e["status"] == "SUCCEEDED"]
    n = 0
    with gzip.open(out, "wt", encoding="utf-8") as g:
        for e in sorted(runs, key=lambda e: e["start"]):
            for line in open(os.path.join(SCRATCH, "runs", e["run_id"] + ".jsonl"), encoding="utf-8"):
                g.write(line)
                n += 1
    print(f"{os.path.basename(out)}: {n} items from runs {[e['run_id'] for e in runs]}")


def cmd_spent(a):
    log = load_log()
    for e in log:
        print(e["run_id"], e["batch"], e["start"], e["end"], e["status"], e["items"], e["cost_usd"])
    print(f"total ${sum(e['cost_usd'] or 0 for e in log):.4f}")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--batch", type=int, required=True)
    r.add_argument("--start", type=int, default=0)
    r.add_argument("--end", type=int)
    r.add_argument("--cap", type=float, required=True)
    r.add_argument("--timeout", type=int, default=6 * 3600)
    r.add_argument("--memory", type=int, default=512)
    ra = sub.add_parser("runall")
    ra.add_argument("--batches", type=int, nargs="+", required=True)
    ra.add_argument("--chunk", type=int, default=500)
    ra.add_argument("--cap", type=float, default=0.16)
    ra.add_argument("--parallel", type=int, default=30)
    ra.add_argument("--timeout", type=int, default=4 * 3600)
    ra.add_argument("--dry", action="store_true")
    s = sub.add_parser("assemble")
    s.add_argument("--batch", type=int, required=True)
    s.add_argument("--force", action="store_true")
    sub.add_parser("spent")
    a = p.parse_args()
    {"run": cmd_run, "runall": cmd_runall, "assemble": cmd_assemble, "spent": cmd_spent}[a.cmd](a)


if __name__ == "__main__":
    main()
