
# clean_markdown.py — Clean and extract documentation for ChatGPT
#
# This script clones a documentation repository, selects and cleans relevant files
# (Markdown/YAML), saves the cleaned versions preserving structure, and logs the changes.
# It supports 'auto' and 'manual-review' execution modes.

import os
import shutil
import yaml
import subprocess
from pathlib import Path
from datetime import datetime

from scripts.utils import clean_text, match_patterns

# Configuration paths
CONFIG_PATH = Path(".clean-docs-for-gpt_config.yml")
STATE_FILE = Path(".clean-docs-for-gpt/last_commit.txt")
LOG_FILE = Path(".clean-docs-for-gpt/cleaning_log.txt")


def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def clone_repo(repo_url):
    """Clone the source repo to a temporary directory and return path + commit hash."""
    tmp_path = Path("tmp_repo")
    if tmp_path.exists():
        shutil.rmtree(tmp_path)
    subprocess.run(["git", "clone", "--depth=1", repo_url, str(tmp_path)], check=True)
    commit = subprocess.check_output(
        ["git", "-C", str(tmp_path), "rev-parse", "HEAD"], text=True
    ).strip()
    return tmp_path, commit


def already_processed(commit_hash):
    """Check if this commit was already processed (to skip reprocessing)."""
    if STATE_FILE.exists():
        return STATE_FILE.read_text(encoding="utf-8").strip() == commit_hash
    return False


def save_commit_hash(commit_hash):
    STATE_FILE.parent.mkdir(exist_ok=True)
    STATE_FILE.write_text(commit_hash, encoding="utf-8")


def write_log(report, summary, commit_hash, repo_url):
    """Generate a human-readable cleaning report."""
    LOG_FILE.parent.mkdir(exist_ok=True)
    with LOG_FILE.open("w", encoding="utf-8") as log:
        log.write(f"# clean-docs-for-gpt – Cleaning Report\n")
        log.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Source repo: {repo_url}\n")
        log.write(f"Source commit: {commit_hash}\n\n")
        log.write(f"--- Files Processed: {len(report)} ---\n\n")
        for item in report:
            log.write(f"✔ {item['path']}\n")
            log.write(f"   Original lines   : {item['original_lines']}\n")
            log.write(f"   Cleaned lines    : {item['cleaned_lines']}\n")
            log.write(f"   Removed lines    : {item['removed_lines']}\n")
            log.write(f"   Original chars   : {item['original_chars']}\n")
            log.write(f"   Cleaned chars    : {item['cleaned_chars']}\n")
            log.write(f"   Removed chars    : {item['removed_chars']}\n")
            log.write(f"   Notes            : {item['notes']}\n\n")

        log.write(f"--- Summary ---\n")
        log.write(f"Total files         : {summary['files']}\n")
        log.write(f"Total lines before  : {summary['lines_before']}\n")
        log.write(f"Total lines after   : {summary['lines_after']}\n")
        log.write(f"Total lines removed : {summary['lines_removed']}\n")
        log.write(f"Total chars before  : {summary['chars_before']}\n")
        log.write(f"Total chars after   : {summary['chars_after']}\n")
        log.write(f"Total chars removed : {summary['chars_removed']}\n")


def clean_docs(repo_url, commit_hash, repo_path, config):
    output_dir = f"{Path(repo_url).name}-clean-docs-for-gpt"
    Path(output_dir).mkdir(exist_ok=True)

    report = []
    summary = {
        "files": 0,
        "lines_before": 0,
        "lines_after": 0,
        "lines_removed": 0,
        "chars_before": 0,
        "chars_after": 0,
        "chars_removed": 0
    }

    for file in repo_path.rglob("*"):
        if not file.is_file():
            continue

        rel_path = file.relative_to(repo_path)
        if not match_patterns(rel_path, config["include"]):
            continue
        if match_patterns(rel_path, config.get("exclude", [])):
            continue
        if file.suffix not in config.get("extensions", []):
            continue

        original = file.read_text(encoding="utf-8")
        cleaned = clean_text(original)

        original_lines = original.count("\n")
        cleaned_lines = cleaned.count("\n")
        original_chars = len(original)
        cleaned_chars = len(cleaned)

        report.append({
            "path": str(rel_path),
            "original_lines": original_lines,
            "cleaned_lines": cleaned_lines,
            "removed_lines": original_lines - cleaned_lines,
            "original_chars": original_chars,
            "cleaned_chars": cleaned_chars,
            "removed_chars": original_chars - cleaned_chars,
            "notes": "basic cleanup"
        })

        summary["files"] += 1
        summary["lines_before"] += original_lines
        summary["lines_after"] += cleaned_lines
        summary["lines_removed"] += original_lines - cleaned_lines
        summary["chars_before"] += original_chars
        summary["chars_after"] += cleaned_chars
        summary["chars_removed"] += original_chars - cleaned_chars

        output_file = Path(output_dir) / rel_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(cleaned, encoding="utf-8")

    write_log(report, summary, commit_hash, repo_url)


def main():
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "auto"
    config = load_config()
    repo_url = config["repo_url"]

    repo_path, commit_hash = clone_repo(repo_url)

    if mode == "manual-review":
        print(f"[INFO] Last commit in {repo_url}: {commit_hash}")
        return

    if mode == "auto" and already_processed(commit_hash):
        print("[INFO] No changes detected, skipping.")
        return

    clean_docs(repo_url, commit_hash, repo_path, config)
    save_commit_hash(commit_hash)

    if mode == "auto":
        print("[INFO] Cleaning complete. Files updated.")
    else:
        print("[INFO] Manual mode complete.")


if __name__ == "__main__":
    main()
