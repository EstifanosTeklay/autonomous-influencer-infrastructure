#!/usr/bin/env python3
"""
Simple automation task runner for developer workflows.
Commands:
  spec-check   -> Runs spec_check.py
  mcp-validate -> Validates mcp/config.yaml
  test         -> Runs pytest tests/functional
  lint         -> Runs ruff (if installed)

Run: python automation/runner.py <command>
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def run(cmd, check=True):
    print(f"$ {cmd}")
    res = subprocess.run(cmd, shell=True)
    if check and res.returncode != 0:
        sys.exit(res.returncode)


def cmd_spec_check():
    run(f"python {ROOT / 'spec_check.py'}")


def cmd_mcp_validate():
    run(f"python {ROOT / 'mcp' / 'validate_config.py'}")


def cmd_test():
    run(f"pytest tests/functional/ -q")


def cmd_lint():
    run("ruff . || true", check=False)


def main():
    if len(sys.argv) < 2:
        print("Usage: runner.py <spec-check|mcp-validate|test|lint>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == 'spec-check':
        cmd_spec_check()
    elif cmd == 'mcp-validate':
        cmd_mcp_validate()
    elif cmd == 'test':
        cmd_test()
    elif cmd == 'lint':
        cmd_lint()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == '__main__':
    main()
