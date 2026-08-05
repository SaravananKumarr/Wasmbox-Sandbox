from typing import Literal

from pydantic import BaseModel


class MarketplaceSearchFilter(BaseModel):
    search: str | None = None
    category: str | None = None
    language: str | None = None

    sort_by: Literal[
        "latest",
        "downloads",
        "views",
        "name",
    ] = "latest"

    page: int = 1
    limit: int = 10