from src.automation.task_reader import fetch_ready_tasks
from src.automation.git_ops import create_or_checkout_branch


def run():
    tasks = fetch_ready_tasks()

    if not tasks:
        return

    task = tasks[0]  # MVP: primeira task

    print(f"\n🚀 Task: {task['title']}")

    branch = create_or_checkout_branch(task["title"])

    print(f"🌿 branch ativa: {branch}")


if __name__ == "__main__":
    run()
