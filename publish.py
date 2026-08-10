#!/usr/bin/env python3
"""
Porsche 993 Daily Digest Publisher
Automated GitHub + Cloudflare Pages deployment
"""

import subprocess
import sys
import os
from pathlib import Path

def run_cmd(cmd, cwd=None):
    """Execute command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"

def main():
    # Set working directory
    repo_dir = Path.home() / "Hermes-Workspace" / "porsche-digest"
    
    if not repo_dir.exists():
        print(f"❌ Directory not found: {repo_dir}")
        return False
    
    os.chdir(repo_dir)
    print(f"📁 Working in: {repo_dir}")
    
    # Load GitHub token from .hermes/.env
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
    
    # Initialize git if needed
    if not (repo_dir / ".git").exists():
        print("🚀 Initializing git repository...")
        
        success, _, error = run_cmd("git init")
        if not success:
            print(f"❌ Git init failed: {error}")
            return False
            
        # Set remote with embedded token
        remote_url = f"https://{github_token}@github.com/zw96v6wxvj-gif/porsche-digest.git"
        success, _, error = run_cmd(f"git remote add origin {remote_url}")
        if not success:
            print(f"❌ Add remote failed: {error}")
            return False
            
        # Configure user (required for commits)
        run_cmd("git config user.email 'hermes@costafamily.ai'")
        run_cmd("git config user.name 'Hermes Carrera'")
    
    # Stage and commit changes
    print("📝 Committing digest update...")
    
    success, _, error = run_cmd("git add .")
    if not success:
        print(f"❌ Git add failed: {error}")
        return False
    
    success, _, error = run_cmd('git commit -m "Daily Porsche 993 digest update - automated via Hermes"')
    if not success and "nothing to commit" not in error:
        print(f"❌ Git commit failed: {error}")
        return False
    
    # Push to GitHub
    print("⬆️  Pushing to GitHub...")
    
    success, stdout, error = run_cmd("git push origin main")
    if not success:
        # Try creating the branch first
        success, _, _ = run_cmd("git push -u origin main")
        if not success:
            print(f"❌ Git push failed: {error}")
            return False
    
    print("✅ Successfully pushed to GitHub!")
    
    # Deploy to Cloudflare Pages via wrangler
    print("🌐 Deploying to Cloudflare Pages...")
    
    # Load Cloudflare credentials
    cf_token = None
    cf_account_id = None
    
    with open(Path.home() / ".hermes" / ".env") as f:
        for line in f:
            if line.startswith("CLOUDFLARE_API_TOKEN="):
                cf_token = line.split("=", 1)[1].strip()
            elif line.startswith("CLOUDFLARE_ACCOUNT_ID="):
                cf_account_id = line.split("=", 1)[1].strip()
    
    if not cf_token or not cf_account_id:
        print("❌ Cloudflare credentials not found in ~/.hermes/.env")
        return False
    
    # Set environment variables for wrangler
    env = os.environ.copy()
    env["CLOUDFLARE_API_TOKEN"] = cf_token
    env["CLOUDFLARE_ACCOUNT_ID"] = cf_account_id
    
    # Deploy with wrangler
    deploy_cmd = "npx wrangler pages deploy . --project-name porsche-digest --branch main"
    
    try:
        result = subprocess.run(deploy_cmd, shell=True, cwd=repo_dir, 
                              capture_output=True, text=True, timeout=120, env=env)
        
        if result.returncode == 0:
            print("✅ Successfully deployed to Cloudflare Pages!")
            print("🔗 Live at: https://digest.costafamily.ai")
            print("🔗 Backup: https://porsche-digest.pages.dev")
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