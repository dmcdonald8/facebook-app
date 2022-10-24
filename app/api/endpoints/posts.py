from typing import Any, Dict, List, Optional

from fastapi import APIRouter

from facebook_scraper import get_posts

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/{account_name}")
def get_facebook_posts(
    account_name: str, pages: Optional[int] = 3
) -> List[Dict[str, Any]]:
    """
    Fetch all Facebook posts for a given account name
    Args:
        account_name: The name of the account
        pages: number of pages to return

    Returns:
        A list of Facebook posts for the given `account_name`
    """
    return list(get_posts(account_name, pages=pages))