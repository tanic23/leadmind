import os
import requests
from dotenv import load_dotenv

load_dotenv()

CALENDLY_API_KEY = os.getenv("CALENDLY_API_KEY")
CALENDLY_USER_URI = os.getenv("CALENDLY_USER_URI")

BASE_URL = "https://api.calendly.com"
HEADERS = {
    "Authorization": f"Bearer {CALENDLY_API_KEY}",
    "Content-Type": "application/json"
}


def get_event_types() -> list:
    """
    Fetch all event types for the authenticated Calendly user.

    Returns:
        List of event type dicts with name, slug, scheduling_url.
    """
    response = requests.get(
        f"{BASE_URL}/event_types",
        headers=HEADERS,
        params={"user": CALENDLY_USER_URI}
    )
    response.raise_for_status()
    data = response.json()
    return [
        {
            "name": et["name"],
            "slug": et["slug"],
            "scheduling_url": et["scheduling_url"],
            "duration": et["duration"]
        }
        for et in data.get("collection", [])
    ]


def get_scheduling_link(event_type_slug: str = None) -> str:
    """
    Get the scheduling URL for a specific event type or the first available one.

    Args:
        event_type_slug: Slug of the event type (e.g. '30-min-call'). Optional.

    Returns:
        Scheduling URL string.
    """
    event_types = get_event_types()
    if not event_types:
        return "[CALENDLY_LINK]"

    if event_type_slug:
        for et in event_types:
            if et["slug"] == event_type_slug:
                return et["scheduling_url"]

    # Default: return first event type URL
    return event_types[0]["scheduling_url"]


def list_scheduled_events(count: int = 10) -> list:
    """
    List upcoming scheduled events.

    Args:
        count: Max number of events to return.

    Returns:
        List of event dicts.
    """
    response = requests.get(
        f"{BASE_URL}/scheduled_events",
        headers=HEADERS,
        params={
            "user": CALENDLY_USER_URI,
            "count": count,
            "status": "active",
            "sort": "start_time:asc"
        }
    )
    response.raise_for_status()
    data = response.json()
    return [
        {
            "name": ev.get("name"),
            "start_time": ev.get("start_time"),
            "end_time": ev.get("end_time"),
            "status": ev.get("status"),
            "uri": ev.get("uri")
        }
        for ev in data.get("collection", [])
    ]


if __name__ == "__main__":
    print("=== Event Types ===")
    event_types = get_event_types()
    for et in event_types:
        print(f"  {et['name']} ({et['duration']} min) → {et['scheduling_url']}")

    print("\n=== Scheduling Link ===")
    link = get_scheduling_link()
    print(f"  {link}")

    print("\n=== Upcoming Events ===")
    events = list_scheduled_events()
    for ev in events:
        print(f"  {ev['name']} | {ev['start_time']} → {ev['end_time']}")
