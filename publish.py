#!/usr/bin/env python3
"""
Porsche 993 Daily Digest — Publisher Script
Generates the daily digest HTML, pushes to GitHub, and deploys to Cloudflare Pages.
Designed to be called by Hermes cronjob.
"""
import os
import sys
import json
import subprocess
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────
REPO_DIR = r"C:\Users\SERVER\Hermes-Workspace\porsche-digest"
REPO_URL = "https://github.com/zw96v6wxvj-gif/porsche-digest.git"
PROJECT_NAME = "porsche-digest"
ACCOUNT_ID = "0a68341689fffbae0284be2321350415"
BRANCH = "main"

# Load tokens from .env — use profile-agnostic path
ENV_PATH = os.path.expanduser("~/.hermes/.env")
# Fallback: profile-specific env
if not os.path.exists(ENV_PATH):
    ENV_PATH = os.path.expanduser("~/.hermes/profiles/hobbies/.env")
env = {}
if os.path.exists(ENV_PATH):
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()

GH_TOKEN = env.get("GITHUB_TOKEN", "")
CF_TOKEN = env.get("CLOUDFLARE_API_TOKEN", "")

def run(cmd, cwd=None, env_vars=None):
    """Run a shell command and return stdout."""
    full_env = os.environ.copy()
    if env_vars:
        full_env.update(env_vars)
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=full_env, cwd=cwd)
    if r.returncode != 0:
        print(f"ERROR: {r.stderr}", file=sys.stderr)
    return r.stdout.strip(), r.stderr.strip(), r.returncode

def publish_html(html_content):
    """Write HTML to repo, commit, push to GitHub, and deploy to Cloudflare Pages."""
    today = datetime.now().strftime("%Y-%m-%d")
    today_br = datetime.now().strftime("%d/%m/%Y")

    # Ensure repo exists
    if not os.path.exists(REPO_DIR):
        run(f'git clone https://{GH_TOKEN}@github.com/zw96v6wxvj-gif/porsche-digest.git "{REPO_DIR}"')

    # Set remote with token for push
    run(f'git remote set-url origin https://{GH_TOKEN}@github.com/zw96v6wxvj-gif/porsche-digest.git',
        cwd=REPO_DIR)

    # Write index.html
    index_path = os.path.join(REPO_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Git commit and push
    run('git add -A', cwd=REPO_DIR)
    run(f'git commit -m "daily digest — {today}"', cwd=REPO_DIR)
    run(f'git push origin {BRANCH}', cwd=REPO_DIR)

    # Deploy to Cloudflare Pages via wrangler
    cf_env = {"CLOUDFLARE_API_TOKEN": CF_TOKEN, "CLOUDFLARE_ACCOUNT_ID": ACCOUNT_ID}
    out, err, rc = run(
        f'npx wrangler pages deploy . --project-name {PROJECT_NAME} --branch {BRANCH}',
        cwd=REPO_DIR, env_vars=cf_env
    )

    # Extract deployment URL from wrangler output
    deploy_url = ""
    for line in out.split("\n"):
        if "Deployment complete" in line or "pages.dev" in line:
            deploy_url = line.strip()
            break

    result = {
        "date": today_br,
        "github": "pushed",
        "cloudflare": deploy_url or "deployed",
        "domain": "https://digest.costafamily.ai",
        "pages_dev": "https://porsche-digest.pages.dev",
        "status": "published"
    }
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    # Test mode: read existing index.html and re-publish
    test_html = os.path.join(REPO_DIR, "index.html")
    if not os.path.exists(test_html):
        test_html = r"C:\Users\SERVER\AppData\Local\Temp\porsche-digest\index.html"
    if os.path.exists(test_html):
        with open(test_html, "r", encoding="utf-8") as f:
            html = f.read()
        publish_html(html)
    else:
        print("No index.html found to publish")
