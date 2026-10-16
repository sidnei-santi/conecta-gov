import os

from dotenv import load_dotenv
from notion_client import Client

load_dotenv()


def get_tasks() -> list[dict[str, str]]:
    token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")

    if not token:
        raise ValueError("NOTION_TOKEN não configurado.")

    if not database_id:
        raise ValueError("NOTION_DATABASE_ID não configurado.")

    notion = Client(auth=token)

    response = notion.databases.query(
        database_id=database_id,
        filter={
            "property": "Status",
            "status": {"equals": "Ready"},
        },
    )

    tasks = []

    for page in response.get("results", []):
        properties = page.get("properties", {})
        title_property = properties.get("Name", {}).get("title", [])
        title = "".join(
            item.get("plain_text", "") for item in title_property
        ).strip()

        if title:
            tasks.append({
                "id": page["id"],
                "title": title,
            })

    return tasks
