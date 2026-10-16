import subprocess


def run(cmd: list[str]) -> str:
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def branch_exists(branch: str) -> bool:
    output = run([
        "git", "branch", "--list",
        "--format=%(refname:short)",
    ])
    return branch in output.splitlines()


def create_or_checkout_branch(name: str) -> str:
    branch = "-".join(name.lower().split())

    if not branch:
        raise ValueError("O nome da branch não pode ser vazio.")

    if branch_exists(branch):
        run(["git", "switch", branch])
    else:
        run(["git", "switch", "-c", branch])

    print(f"Branch local selecionada: {branch}")
    return branch


def commit_files(paths: list[str], message: str) -> None:
    if not paths:
        raise ValueError("Informe explicitamente os arquivos do commit.")

    if not message.strip():
        raise ValueError("A mensagem do commit não pode ser vazia.")

    run(["git", "add", "--", *paths])

    staged = run(["git", "diff", "--cached", "--name-only"])
    if not staged:
        raise RuntimeError("Nenhuma alteração preparada para commit.")

    run(["git", "commit", "-m", message])


def push(branch: str) -> None:
    if not branch or branch == "main":
        raise ValueError("Push bloqueado: informe uma branch de trabalho.")

    run(["git", "push", "-u", "origin", branch])
