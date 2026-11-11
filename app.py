"""An original synthetic print-desk API for a Copilot Studio topic/connector example."""
from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent
JOBS = (
    {"jobId": "JOB-101", "title": "Garden club booklet", "status": "Awaiting proof approval", "readyAt": ""},
    {"jobId": "JOB-102", "title": "Garden club poster", "status": "Ready for collection", "readyAt": "Ready now in this synthetic snapshot"},
    {"jobId": "JOB-103", "title": "Paper lantern instructions", "status": "Queued for printing", "readyAt": ""},
)


def lookup(query: str) -> dict:
    if not isinstance(query, str) or not 1 <= len(query.strip()) <= 80:
        raise ValueError("Use a query of 1 to 80 characters.")
    query.encode("utf-8")
    if any(ord(c) < 32 or ord(c) == 127 for c in query):
        raise ValueError("Control characters are not supported.")
    query = query.strip().casefold()
    # An identifier never silently falls back to an unrelated title match.
    exact = [j for j in JOBS if j["jobId"].casefold() == query]
    matches = exact or ([j for j in JOBS if all(w in j["title"].casefold() for w in query.split())]
                        if not query.startswith("job-") else [])
    result = dict(outcome="not_found", sourceId="", jobId="", title="", status="", readyAt="", candidateIds=[],
                  message="No matching synthetic print job. Check the job ID; no status was inferred.")
    if len(matches) > 1:
        ids = [j["jobId"] for j in matches]
        result.update(outcome="ambiguous", candidateIds=ids,
                      message="Several jobs match: " + ", ".join(ids) + ". Start print status again with an exact job ID.")
    elif matches:
        job = matches[0]
        source = "print-snapshot/" + job["jobId"]
        result.update(job, outcome="found", sourceId=source,
                      message=f"{job['jobId']} — {job['title']}: {job['status']}. "
                      f"Collection timing: {job['readyAt'] or 'not confirmed'}. [Source: {source}]")
    return result


def evaluate(cases_path: Path | None = None) -> dict:
    """Check the reference API contract, not a language model or cloud agent."""
    cases = json.loads((cases_path or ROOT / "evaluation/cases.json").read_text(encoding="utf-8"))
    results = []
    for case in cases:
        actual = lookup(case["query"])
        passed = all(actual[key] == value for key, value in case["expected"].items())
        passed = passed and all(word not in actual["message"] for word in case.get("forbidden", []))
        results.append({"id": case["id"], "passed": passed, "outcome": actual["outcome"]})
    return {"scope": "synthetic API reference cases only; Copilot Studio not executed",
            "passed": sum(r["passed"] for r in results), "total": len(results), "results": results}


def make_server(port: int = 8767):
    class Handler(BaseHTTPRequestHandler):
        server_version = "SyntheticPrintDesk"
        sys_version = ""

        def setup(self):
            super().setup()
            self.connection.settimeout(5)

        def log_message(self, *args):
            pass

        def reply(self, status, body):
            raw = json.dumps(body, ensure_ascii=True).encode("ascii")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            try:
                self.wfile.write(raw)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def do_GET(self):
            if self.headers.get_all("Host", []) not in ([f"127.0.0.1:{self.server.server_port}"], [f"localhost:{self.server.server_port}"]):
                self.reply(403, {"error": "Use the loopback URL printed by the server."})
                return
            try:
                url = urlsplit(self.path)
                params = parse_qs(url.query, keep_blank_values=True, encoding="utf-8", errors="strict", max_num_fields=4)
                if url.path == "/health" and not params:
                    self.reply(200, {"status": "ok", "scope": "synthetic local API only"})
                elif url.path == "/lookup":
                    if set(params) != {"query"} or len(params["query"]) != 1:
                        raise ValueError("Supply exactly one query parameter.")
                    self.reply(200, lookup(params["query"][0]))
                else:
                    self.reply(404, {"error": "Route not found."})
            except (ValueError, UnicodeError):
                self.reply(400, {"error": "Use one valid query of 1 to 80 characters."})

        def do_POST(self):
            self.reply(405, {"error": "This API exposes read-only GET operations."})

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    find = sub.add_parser("lookup", help="Look up an invented print job without network access")
    find.add_argument("query")
    sub.add_parser("evaluate", help="Execute synthetic reference cases, not a Copilot agent")
    serve = sub.add_parser("serve", help="Run a loopback-only read-only API")
    serve.add_argument("--port", type=int, default=8767)
    args = parser.parse_args(argv)
    try:
        if args.command == "lookup":
            print(json.dumps(lookup(args.query), ensure_ascii=True, indent=2))
            return 0
        if args.command == "evaluate":
            report = evaluate()
            print(json.dumps(report, indent=2))
            return 0 if report["passed"] == report["total"] else 1
        if not 0 <= args.port <= 65535:
            parser.error("Port must be between 0 and 65535.")
        with make_server(args.port) as server:
            print(f"Synthetic print API: http://127.0.0.1:{server.server_port}", flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass
        return 0
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
