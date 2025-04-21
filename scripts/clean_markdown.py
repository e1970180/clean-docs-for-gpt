
# clean_markdown.py — Process multiple documentation targets from external config
import os
import sys
import shutil
import fnmatch
import subprocess
import yaml
from pathlib import Path
from datetime import datetime

def clean_text(text):
    return '\n'.join(line.rstrip() for line in text.splitlines() if line.strip())

def match_patterns(path, patterns):
    if not patterns:
        return False
    return any(fnmatch.fnmatch(path.as_posix(), pattern) for pattern in patterns)

def clone_repo(repo_url, workdir):
    tmp_path = workdir / f"tmp_repo_{Path(repo_url).name.replace('.', '_')}"
    if tmp_path.exists():
        shutil.rmtree(tmp_path)
    subprocess.run(["git", "clone", "--depth=1", repo_url, str(tmp_path)], check=True)
    commit = subprocess.check_output(["git", "-C", str(tmp_path), "rev-parse", "HEAD"], text=True).strip()
    return tmp_path, commit

def write_log(log_dir, report, summary, commit_hash, repo_url):
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "cleaning_log.txt"
    with log_path.open("w", encoding="utf-8") as log:
        log.write(f"# Cleaning Report\n")
        log.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Repo: {repo_url}\n")
        log.write(f"Commit: {commit_hash}\n\n")
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

def clean_target(target, workdir):
    repo_url = target["repo_url"]
    include = target["include"]
    exclude = target.get("exclude", [])
    extensions = target.get("extensions", [])

    tmp_repo, commit = clone_repo(repo_url, workdir)
    out_dir = Path(f"{Path(repo_url).name}-clean-docs-for-gpt")
    out_dir.mkdir(exist_ok=True)

    report = []
    summary = dict(files=0, lines_before=0, lines_after=0, lines_removed=0,
                   chars_before=0, chars_after=0, chars_removed=0)

    for file in tmp_repo.rglob("*"):
        if not file.is_file():
            continue
        rel_path = file.relative_to(tmp_repo)
        if not match_patterns(rel_path, include):
            print(f"[SKIP] {rel_path} not in include")
            continue
        if match_patterns(rel_path, exclude):
            print(f"[SKIP] {rel_path} excluded")
            continue
        if file.suffix not in extensions:
            print(f"[SKIP] {rel_path} unsupported extension")
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

        out_path = out_dir / rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(cleaned, encoding="utf-8")

    write_log(out_dir, report, summary, commit, repo_url)
    shutil.rmtree(tmp_repo, ignore_errors=True)
    print(f"[DONE] {repo_url} processed.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python clean_markdown.py <path-to-config>")
        return

    config_path = Path(sys.argv[1])
    if not config_path.exists():
        print(f"[ERROR] Config not found: {config_path}")
        return

    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    workdir = Path(".clean-docs-for-gpt")
    workdir.mkdir(exist_ok=True)

    for target in config.get("targets", []):
        clean_target(target, workdir)

if __name__ == "__main__":
    main()
