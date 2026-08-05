from datetime import datetime
from datetime import timezone


def humanize_relative(dt: datetime) -> str:
    """Formats a datetime as a short relative string ("2 min ago"), matching
    the timestamps the frontend previously received from its mock data.
    """
    if dt is None:
        return "--"

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    delta_seconds = (datetime.now(timezone.utc) - dt).total_seconds()

    if delta_seconds < 0:
        delta_seconds = 0

    if delta_seconds < 60:
        return "Just now"

    minutes = int(delta_seconds // 60)
    if minutes < 60:
        return f"{minutes} min ago"

    hours = int(minutes // 60)
    if hours < 24:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"

    days = int(hours // 24)
    return f"{days} day{'s' if days != 1 else ''} ago"
