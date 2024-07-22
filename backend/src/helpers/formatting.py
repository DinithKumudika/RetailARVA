# Function to format lists into a multiline string
from typing import List, Optional


def format_list(items: Optional[List[str]]) -> str:
    if items is None:
        return "None"
    return "\n".join(f"- {item}" for item in items)

def sqlalchemy_to_dict(instance):
    return {c.name: getattr(instance, c.name) for c in instance.__table__.columns}