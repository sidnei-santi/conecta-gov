from src.automation.notion_client import get_tasks


def fetch_ready_tasks():
    tasks = get_tasks()

    if not tasks:
        print("Nenhuma task encontrada")
        return []

    print("TASKS ENCONTRADAS:")
    for t in tasks:
        print("-", t["title"])

    return tasks
