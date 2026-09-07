import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

def run_pytest():
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_security.py",
        "-v",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def main():
    print("=" * 60)
    print("Running security tests...")
    print("=" * 60)

    result = run_pytest()

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    report_path = REPORT_DIR / "security_report.txt"
    report_path.write_text(
        result.stdout + "\n" + result.stderr,
        encoding="utf-8",
    )

    print(f"Report saved: {report_path}")

    return result.returncode

if __name__ == "__main__":
    sys.exit(main())