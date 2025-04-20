# clean_markdown.py
#
# Этот скрипт:
# 1. Загружает внешний репозиторий (shallow clone)
# 2. Проверяет commit HEAD
# 3. Если commit не изменился — завершает работу
# 4. Если commit изменился:
#     - очищает указанные файлы от markdown-шумов (html, изображения, ссылки)
#     - сохраняет в <repo_name>-clean-docs-for-gpt/
#     - коммитит и пушит результат
#
# Поддерживает два режима запуска:
# - auto (по умолчанию): сразу выполняет все действия
# - manual-review: выводит commit и завершает, без изменений

import os
import yaml
import re
import shutil
import fnmatch
import subprocess
from pathlib import Path
import sys

CONFIG_PATH = Path(".clean-docs-for-gpt_config.yml")
STATE_FILE = Path(".clean-docs-for-gpt/last_source_commit.txt")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_latest_commit(repo_url):
    # Получить текущий хэш HEAD оригинального репозитория
    output = subprocess.check_output(["git", "ls-remote", repo_url, "HEAD"], text=True)
    return output.split()[0]

def get_last_processed_commit():
    # Считать предыдущий обработанный commit из файла состояния
    if STATE_FILE.exists():
        return STATE_FILE.read_text().strip()
    return None

def save_commit(commit_hash):
    # Сохранить текущий хэш в файл состояния
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(commit_hash)

def match_patterns(path, patterns):
    # Проверка путей по шаблонам include/exclude
    return any(fnmatch.fnmatch(path.as_posix(), pattern) for pattern in patterns)

def clean_content(content, ext):
    # Очистка markdown-файлов от лишнего
    if ext in [".md", ".markdown"]:
        content = re.sub(r"!\[.*?\]\(.*?\)", "", content)
        content = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", content)
        content = re.sub(r"<[^>]+>", "", content)
    return content

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "auto"
    cfg = load_config()
    repo_url = cfg["repo_url"]
    include = cfg.get("include", [])
    exclude = cfg.get("exclude", [])
    extensions = cfg.get("extensions", [])

    latest_commit = get_latest_commit(repo_url)
    last_commit = get_last_processed_commit()

    if last_commit == latest_commit:
        print("✅ Documentation is up to date. No changes detected.")
        return

    if mode == "manual-review":
        print("🔍 New commit detected:", latest_commit)
        print("Previous commit was:", last_commit)
        print("Please review manually before continuing.")
        return

    repo_name = repo_url.rstrip("/").split("/")[-1]
    output_root = Path(f"{repo_name}-clean-docs-for-gpt")
    if output_root.exists():
        shutil.rmtree(output_root)

    os.system(f"git clone --depth=1 {repo_url} tmp_repo")
    base_path = Path("tmp_repo")

    for file in base_path.rglob("*"):
        if not file.is_file() or file.suffix not in extensions:
            continue
        rel_path = file.relative_to(base_path)
        if not match_patterns(rel_path, include) or match_patterns(rel_path, exclude):
            continue
        out_path = output_root / rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file, "r", encoding="utf-8", errors="ignore") as f_in:
            raw = f_in.read()
            cleaned = clean_content(raw, file.suffix)
        with open(out_path, "w", encoding="utf-8") as f_out:
            f_out.write(cleaned)

    shutil.rmtree("tmp_repo")

    save_commit(latest_commit)

    os.system("git config user.name 'github-actions[bot]'")
    os.system("git config user.email 'github-actions[bot]@users.noreply.github.com'")
    os.system("git add .")
    os.system(f"git commit -m 'docs: update cleaned docs from {latest_commit}' || echo 'Nothing to commit'")
    os.system("git push")

if __name__ == "__main__":
    main()