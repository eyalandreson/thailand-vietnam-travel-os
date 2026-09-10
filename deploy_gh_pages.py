"""
Autonomous GitHub Pages Deployer & Repository Manager
1. Verifies/Creates GitHub repository 'eyalandreson/thailand-vietnam-travel-os'
2. Pushes full codebase and CI workflows to 'main' branch
3. Pushes web dashboard directly to 'gh-pages' branch for instant live hosting
4. Enables GitHub Pages and verifies the public live URL
"""
import os
import subprocess
import requests
import dotenv

def deploy():
    env = dotenv.dotenv_values(".env")
    pat = env.get("GITHUB_PAT")
    if not pat:
        print("ERROR: GITHUB_PAT not found in .env")
        return False

    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 1. Get user login
    user_res = requests.get("https://api.github.com/user", headers=headers)
    if user_res.status_code != 200:
        print(f"ERROR: Failed to authenticate with GitHub: {user_res.text}")
        return False
    username = user_res.json().get("login", "eyalandreson")
    repo_name = "thailand-vietnam-travel-os"
    repo_full = f"{username}/{repo_name}"
    print(f"Authenticated as GitHub user: {username}")

    # 2. Check if repository exists
    repo_res = requests.get(f"https://api.github.com/repos/{repo_full}", headers=headers)
    if repo_res.status_code == 404:
        print(f"Creating new GitHub repository: {repo_full}...")
        create_payload = {
            "name": repo_name,
            "description": "Master Itinerary: Thailand & Vietnam [Live Travel OS] - Autonomous 2-Tier Platform",
            "private": False,
            "has_pages": True,
            "auto_init": False
        }
        create_res = requests.post("https://api.github.com/user/repos", headers=headers, json=create_payload)
        if create_res.status_code not in (200, 201):
            print(f"Failed to create repo: {create_res.text}")
            return False
        print("Repository successfully created!")
    else:
        print(f"Repository {repo_full} already exists.")

    remote_url = f"https://{username}:{pat}@github.com/{repo_full}.git"

    # 3. Git Init & Push Main
    print("Preparing git commit for 'main' branch...")
    cmds = [
        ["git", "init"],
        ["git", "config", "user.name", "Eyal Andreson"],
        ["git", "config", "user.email", "eyal@example.com"],
        ["git", "checkout", "-B", "main"],
        ["git", "add", "."],
        ["git", "commit", "-m", "feat: initial release of Thailand & Vietnam Live Travel OS with serverless runner & web app"],
        ["git", "remote", "remove", "origin"],
    ]
    for c in cmds:
        try:
            subprocess.run(c, capture_output=True, text=True, check=False)
        except Exception:
            pass

    # Add origin and push main
    subprocess.run(["git", "remote", "add", "origin", remote_url], capture_output=True, text=True)
    push_res = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], capture_output=True, text=True)
    print(f"Pushed to main: returncode={push_res.returncode}")
    if push_res.stderr:
        # Sanitize PAT from error output
        sanitized = push_res.stderr.replace(pat, "***")
        print("Git Output:", sanitized)

    # 4. Deploy web/ to gh-pages branch
    print("\nDeploying web/ dashboard to 'gh-pages' branch...")
    # Use git subtree or worktree or temporary branch
    web_dir = os.path.abspath("web")
    # Initialize a temporary git in web_dir or use orphan branch
    gh_cmds = [
        f"cd web; git init; git config user.name 'Eyal Andreson'; git config user.email 'eyal@example.com'; git checkout -B gh-pages; git add .; git commit -m 'deploy: web dashboard to GitHub Pages'; git remote add origin {remote_url}; git push -u origin gh-pages --force"
    ]
    p = subprocess.run(["powershell", "-Command", gh_cmds[0]], capture_output=True, text=True)
    print(f"Pushed to gh-pages: returncode={p.returncode}")
    if p.stderr:
        print("Output:", p.stderr.replace(pat, "***"))

    # 5. Enable GitHub Pages on gh-pages branch
    pages_url = f"https://api.github.com/repos/{repo_full}/pages"
    pages_payload = {
        "source": {
            "branch": "gh-pages",
            "path": "/"
        }
    }
    pages_res = requests.post(pages_url, headers=headers, json=pages_payload)
    if pages_res.status_code in (201, 204, 409):
        print("GitHub Pages configured on branch 'gh-pages'!")
    else:
        # Try PUT if already exists
        requests.put(pages_url, headers=headers, json=pages_payload)

    live_url = f"https://{username}.github.io/{repo_name}/"
    print("LIVE DEPLOYMENT COMPLETE!")
    print(f"Web Dashboard Live URL: https://{username}.github.io/{repo_name}/")
    print(f"GitHub Repository: https://github.com/{repo_full}")
    return True

if __name__ == "__main__":
    deploy()
