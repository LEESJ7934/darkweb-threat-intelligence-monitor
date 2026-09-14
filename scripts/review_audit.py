"""Read-only aggregate review of governance audit logs."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from governance.audit_review import AuditReviewError, DEFAULT_DAYS, review


def parser():
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--days", type=int, default=DEFAULT_DAYS, help="UTC review window (default: 30)")
    value.add_argument("--log-dir", default=None, help="Audit directory; defaults to repository logs/")
    value.add_argument("--json", action="store_true", help="Emit aggregate JSON")
    return value


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        result = review(args.log_dir, days=args.days)
    except AuditReviewError as error:
        print(f"ERROR: {error}")
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))
    else:
        print(f"Audit review: {result['status']}")
        print(f"Window: {result['window_days']} day(s), files={result['files_reviewed']}, records={result['counts']['records_in_window']}")
        for name in ("login_failure", "denied_access", "error", "retention_error", "malformed"):
            marker = "ATTENTION" if result["breaches"][name] else "OK"
            print(f"- {name}: {result['counts'][name]} / threshold {result['thresholds'][name]} [{marker}]")
        print("Privacy: aggregate counts only; raw user/document identifiers are not printed.")
    return 1 if result["status"] == "ATTENTION" else 0


if __name__ == "__main__":
    raise SystemExit(main())
