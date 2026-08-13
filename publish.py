#!/usr/bin/env python3
"""
Porsche 993 Daily Digest Publisher
Automated GitHub + Cloudflare Pages deployment with historical archive.
"""

import subprocess
import sys
import os
import hashlib
import re
from pathlib import Path
from datetime import datetime


def run_cmd(cmd, cwd=None, timeout=60):
    """Execute command and return result."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"


def extract_date_from_html(html):
    """Extract the date from the digest HTML hero section."""
    match = re.search(r'<div class="date">(.+?)</div>', html)
    if match:
        return match.group(1)
    return ""


def generate_history_section(archive_dir):
    """Generate HTML for the history section from archived digests."""
    if not os.path.exists(archive_dir):
        return ""

    archives = sorted(
        [f for f in os.listdir(archive_dir) if f.endswith('.html')],
        reverse=True  # newest first
    )

    if not archives:
        return ""

    items = []
    for archive_file in archives:
        date_str = archive_file.replace('.html', '')
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            pretty_date = date_obj.strftime("%d %b %Y")
        except ValueError:
            pretty_date = date_str

        items.append(f'''
        <li class="history-item">
            <a href="/archive/{archive_file}" class="history-link">{pretty_date}</a>
            <span class="history-date">{date_str}</span>
        </li>''')

    return f'''
    <div class="section">
        <div class="section-title">
            <span class="icon">📚</span> Arquivo Histórico de Digests
        </div>
        <ul class="history-list">
            {''.join(items)}
        </ul>
    </div>'''


def inject_history_into_html(html, history_html):
    """Inject the history section before the SOURCES section."""
    # Insert history section before the Sources section
    marker = '<div class="section">\n            <div class="section-title">\n                <span class="icon">📎</span> Fontes'
    if marker in html and history_html:
        html = html.replace(marker, history_html + '\n\n        <!-- SOURCES -->\n' + marker)
    elif history_html:
        # Append at end before closing container
        html = html.replace('</div>\n    </div>\n\n    <div class="footer">', history_html + '\n\n        </div>\n    </div>\n\n    <div class="footer">')
    return html


def main():
    # Set working directory
    repo_dir = Path.home() / "Hermes-Workspace" / "porsche-digest"

    if not repo_dir.exists():
        print(f"❌ Directory not found: {repo_dir}")
        return False

    os.chdir(repo_dir)
    print(f"📁 Working in: {repo_dir}")

    # --- STEP 1: Archive current index.html ---
    index_path = repo_dir / "index.html"
    archive_dir = repo_dir / "archive"
    archive_dir.mkdir(exist_ok=True)

    if index_path.exists():
        # Read HTML to get the date
        with open(index_path, 'r', encoding='utf-8') as f:
            current_html = f.read()

        date_text = extract_date_from_html(current_html)
        today = datetime.now().strftime("%Y-%m-%d")

        # Archive with today's date
        archive_file = archive_dir / f"{today}.html"

        # Check if content has changed
        current_hash = hashlib.md5(current_html.encode()).hexdigest()

        if archive_file.exists():
            with open(archive_file, 'r', encoding='utf-8') as f:
                archived_hash = hashlib.md5(f.read().encode()).hexdigest()

            if current_hash == archived_hash:
                print(f"⚠️  Already archived for today ({today}) — skipping duplicate")
            else:
                # Overwrite with new content
                with open(archive_file, 'w', encoding='utf-8') as f:
                    f.write(current_html)
                print(f"✅ Updated archive: {archive_file.name}")
        else:
            with open(archive_file, 'w', encoding='utf-8') as f:
                f.write(current_html)
            print(f"✅ Archived current digest to: archive/{today}.html")

    # --- STEP 2: Inject history section into index.html ---
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            html = f.read()

        history_html = generate_history_section(str(archive_dir))

        if history_html:
            # Only inject if not already present
            if 'Arquivo Histórico de Digests' not in html:
                html = inject_history_into_html(html, history_html)

                # Add CSS for history section
                history_css = '''
        /* History Section */
        .history-list { list-style: none; padding-left: 0; }
        .history-item { padding: 8px 0; border-bottom: 1px solid var(--carbon); }
        .history-link {
            color: var(--gold);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
        }
        .history-link:hover { color: var(--signal); text-shadow: 0 0 8px var(--signal); }
        .history-date {
            float: right;
            color: var(--guard);
            font-size: 0.8rem;
        }
'''
                # Insert CSS before the Sources section
                html = html.replace('        /* Sources */', history_css + '\n        /* Sources */')

                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(html)
                print("✅ Injected history section into index.html")

    # --- STEP 3: Load tokens ---
    env_file = Path.home() / ".hermes" / ".env"
    github_token = None

    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.startswith("GITHUB_TOKEN="):
                    github_token = line.split("=", 1)[1].strip()
                    break

    if not github_token:
        print("❌ GITHUB_TOKEN not found in ~/.hermes/.env")
        return False

    # --- STEP 4: Git operations ---
    if not (repo_dir / ".git").exists():
        print("🚀 Initializing git repository...")
        success, _, error = run_cmd("git init")
        if not success:
            print(f"❌ Git init failed: {error}")
            return False

        remote_url = f"https://***@github.com/zw96v6wxvj-gif/porsche-digest.git"
        success, _, error = run_cmd(f"git remote add origin {remote_url}")
        if not success:
            print(f"❌ Add remote failed: {error}")
            return False

        run_cmd("git config user.email 'hermes@costafamily.ai'")
        run_cmd("git config user.name 'Hermes Carrera'")

    print("📝 Committing digest update...")
    success, _, error = run_cmd("git add .")
    if not success:
        print(f"❌ Git add failed: {error}")
        return False

    commit_msg = f"Daily Porsche 993 digest — {datetime.now().strftime('%d/%m/%Y')} — automated via Hermes + archive"
    success, _, error = run_cmd(f'git commit -m "{commit_msg}"')
    if not success and "nothing to commit" not in error:
        print(f"❌ Git commit failed: {error}")
        return False

    # Push to GitHub
    print("⬆️  Pushing to GitHub...")
    success, stdout, error = run_cmd("git push origin main", timeout=120)
    if not success:
        success, _, _ = run_cmd("git push -u origin main", timeout=120)
        if not success:
            print(f"❌ Git push failed: {error}")
            return False

    print("✅ Successfully pushed to GitHub!")

    # --- STEP 5: Deploy to Cloudflare Pages ---
    print("🌐 Deploying to Cloudflare Pages...")
    cf_token = None
    cf_account_id = None

    with open(env_file) as f:
        for line in f:
            if line.startswith("CLOUDFLARE_API_TOKEN="):
                cf_token = line.split("=", 1)[1].strip()
            elif line.startswith("CLOUDFLARE_ACCOUNT_ID="):
                cf_account_id = line.split("=", 1)[1].strip()

    if not cf_token or not cf_account_id:
        print("❌ Cloudflare credentials not found in ~/.hermes/.env")
        return False

    env = os.environ.copy()
    env["CLOUDFLARE_API_TOKEN"] = cf_token
    env["CLOUDFLARE_ACCOUNT_ID"] = cf_account_id

    deploy_cmd = f"npx wrangler pages deploy . --project-name porsche-digest-v2 --branch v2-redesign"

    try:
        result = subprocess.run(deploy_cmd, shell=True, cwd=repo_dir,
                              capture_output=True, text=True, timeout=120, env=env)

        if result.returncode == 0:
            print("✅ Successfully deployed to Cloudflare Pages!")
            print("🔗 Live at: https://porscheV2digest.costafamily.ai")
            print("🔗 Backup: https://porsche-digest-v2.pages.dev")
            print("🔗 Archive: https://porscheV2digest.costafamily.ai/archive/")
            return True
        else:
            print(f"❌ Wrangler deploy failed: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Wrangler deploy timed out")
        return False
    except FileNotFoundError:
        print("❌ wrangler not found. Install with: npm install -g wrangler")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)