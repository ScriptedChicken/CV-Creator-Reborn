import re
import subprocess


class FreeUsageLimitError(Exception):
    pass


def ask_opencode(prompt: str) -> str:
    result = subprocess.run(
        ["opencode", "run", prompt],
        capture_output=True,
        text=True,
    )

    combined = result.stderr + "\n" + result.stdout

    if result.returncode != 0 or "freeusagelimiterror" in combined.lower():
        error_msg = result.stderr.strip() or result.stdout.strip()
        message_match = re.search(
            r'"message"\s*:\s*"([^"]+)"',
            combined,
        )
        if message_match and "freeusagelimiterror" in combined.lower():
            raise FreeUsageLimitError(message_match.group(1))
        if "freeusagelimiterror" in combined.lower():
            raise FreeUsageLimitError(error_msg)
        if result.returncode != 0:
            raise RuntimeError(
                f"opencode failed (exit {result.returncode}): {error_msg}"
            )

    output = result.stdout.strip()
    output = re.sub(r"\x1b\[[0-9;]*m", "", output)
    lines = [l for l in output.split("\n") if l and not l.startswith(">")]
    return "\n".join(lines).strip()
