import os

from dotenv import load_dotenv
from github import Auth, Github
from github.GithubException import GithubException

load_dotenv()


class GitHubPREngine:
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        repo_name = os.getenv("GITHUB_REPO")

        if not token or not repo_name:
            raise ValueError(
                "Configure GITHUB_TOKEN e GITHUB_REPO no ambiente."
            )

        self.gh = Github(auth=Auth.Token(token))
        self.repo = self.gh.get_repo(repo_name)

    def branch_exists(self, branch: str) -> bool:
        try:
            self.repo.get_branch(branch)
            return True
        except GithubException as exc:
            if exc.status == 404:
                return False
            raise

    def find_open_pr(self, branch: str):
        pulls = self.repo.get_pulls(
            state="open",
            head=f"{self.repo.owner.login}:{branch}",
            base="main",
        )
        return next(iter(pulls), None)

    def ensure_branch_and_pr(
        self,
        branch: str,
        title: str,
        body: str = "",
    ) -> str | None:
        if not self.branch_exists(branch):
            print(
                f"Branch remota '{branch}' não encontrada. "
                "Envie a branch antes de criar o PR."
            )
            return None

        existing_pr = self.find_open_pr(branch)
        if existing_pr:
            print(f"PR aberto já existe: {existing_pr.html_url}")
            return existing_pr.html_url

        pr = self.repo.create_pull(
            title=title,
            body=body or f"Pull request for {title}",
            head=branch,
            base="main",
        )

        print(f"PR criado: {pr.html_url}")
        return pr.html_url
