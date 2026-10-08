from datetime import datetime


def iso_utc(dt: datetime | None) -> str | None:
    """Timestamps are stored as naive UTC; send them with an explicit Z so browsers convert correctly."""
    return dt.isoformat() + "Z" if dt else None
