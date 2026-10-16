import os
import subprocess

from dotenv import load_dotenv
from src.automation.github_pr_engine import GitHubPREngine

load_dotenv()


def main():
    # Descobre a branch atual do Git
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True,
        check=True,
    )
    branch = result.stdout.strip()

    # Evita criar PR acidentalmente a partir da main
    if not branch or branch == "main":
        raise RuntimeError(
            "Você está na main. Mude para uma branch de trabalho antes de criar o PR."
        )

    title = os.getenv(
        "GITHUB_PR_TITLE",
        f"feat: {branch.replace('-', ' ')}",
    )

    print(f"🔍 Branch identificada: {branch}")
    print(f"📝 Título do PR: {title}")

    engine = GitHubPREngine()

    pr_url = engine.ensure_branch_and_pr(
        branch=branch,
        title=title,
        body="Auto-generated PR from FDE pipeline",
    )

    if pr_url:
        print(f"✅ PR criado: {pr_url}")
    else:
        print("⚠️ PR não criado. Verifique as mensagens acima.")


if __name__ == "__main__":
    main()
