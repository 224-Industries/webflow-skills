#!/usr/bin/env python3
"""
Safe wrapper for memberstack-cli commands.
Adds boundary markers around CLI output and basic sanitization
to mitigate prompt injection from untrusted API data.

Usage:
    python run_memberstack.py <command> [args...]

Examples:
    python run_memberstack.py members list --json
    python run_memberstack.py records list <table-id>
    python run_memberstack.py whoami
"""

import sys
import re
import subprocess
import shutil

DESTRUCTIVE_COMMANDS = {
    ("members", "delete"),
    ("members", "bulk-delete"),
    ("members", "bulk-update"),
    ("members", "bulk-add-plan"),
    ("members", "bulk-remove-plan"),
    ("plans", "delete"),
    ("apps", "delete"),
    ("tables", "delete"),
    ("records", "delete"),
    ("records", "bulk-delete"),
    ("records", "bulk-update"),
    ("custom-fields", "delete"),
}

_INJECTION_RE = re.compile(
    r"(?:you are|you must|ignore previous|disregard|forget all|override|"
    r"system:|<\||<system>|</?instruction)",
    re.IGNORECASE,
)


SENSITIVE_PATHS = [
    "auth.json",
    ".memberstack",
    "credentials",
    "token",
]


def find_cli() -> list[str]:

    which = shutil.which("memberstack-cli") or shutil.which("memberstack")
    if which:
        return [which]

    return ["npx", "memberstack-cli"]


def is_destructive(args: list[str]) -> bool:

    if len(args) < 2:
        return False
    cmd_pair = (args[0], args[1])
    return cmd_pair in DESTRUCTIVE_COMMANDS


def uses_live_flag(args: list[str]) -> bool:

    return "--live" in args


def sanitize_output(text: str) -> str:

    lines = text.splitlines()
    sanitized = []
    for line in lines:
        if _INJECTION_RE.search(line):
            sanitized.append(f"[SANITIZED — suspicious content removed]: {line[:50]}...")
        else:
            sanitized.append(line)
    return "\n".join(sanitized)


def check_for_sensitive_args(args: list[str]) -> bool:

    full_cmd = " ".join(args).lower()
    for sensitive in SENSITIVE_PATHS:
        if sensitive in full_cmd:
            print(f"Error: Command references a sensitive path ({sensitive}). Aborting.")
            return True
    return False


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    args = sys.argv[1:]

    if check_for_sensitive_args(args):
        sys.exit(1)

    confirmed = "--confirmed" in args
    cli_args = [a for a in args if a != "--confirmed"]

    if is_destructive(cli_args) and not confirmed:
        env_label = "LIVE" if uses_live_flag(cli_args) else "SANDBOX"
        print(f"DESTRUCTIVE COMMAND detected ({env_label} environment):")
        print(f"    memberstack {' '.join(cli_args)}")
        print()
        print("Confirm with the user before proceeding.")
        print("Re-run with --confirmed after user approval:")
        print(f"    python run_memberstack.py {' '.join(cli_args)} --confirmed")
        print("--- COMMAND NOT EXECUTED (requires confirmation) ---")
        sys.exit(2)

    args = cli_args

    cmd_parts = find_cli() + args

    try:
        result = subprocess.run(
            cmd_parts,
            capture_output=True,
            text=True,
            timeout=60,
        )


        if result.stdout.strip():
            sanitized = sanitize_output(result.stdout)
            print("--- BEGIN MEMBERSTACK CLI OUTPUT ---")
            print(sanitized)
            print("--- END MEMBERSTACK CLI OUTPUT ---")

        if result.stderr.strip():

            sanitized_err = sanitize_output(result.stderr)
            print("--- BEGIN MEMBERSTACK CLI ERRORS ---")
            print(sanitized_err)
            print("--- END MEMBERSTACK CLI ERRORS ---")

        sys.exit(result.returncode)

    except FileNotFoundError:
        print("Error: memberstack-cli not found. Install with: npm install -g memberstack-cli")
        print("       Or use npx: npx memberstack-cli <command>")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Error: Command timed out after 60 seconds.")
        sys.exit(1)


if __name__ == "__main__":
    main()