from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Depends
from pydantic import AnyHttpUrl

from services.facebook import FacebookClient

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/raw/{account_name}")
def get_facebook_posts(
    account_name: str,
    pages: Union[int, None] = 3,
    date: Union[int, None] = None,
    client: FacebookClient = Depends(FacebookClient),
) -> List[Dict[str, Any]]:
    """
    Fetch all Facebook posts for a given account name

    Args:
        account_name: The name of the account
        pages: number of pages to return
        date: Date to filter posts by in the format "YYYY-DD-MM"
        client: An instance of `FacebookClient`
    Returns:
        A list of Facebook posts for the given `account_name`
    """
    return client.get_raw_posts(account_name, pages=pages, date=date)


@router.get("/thumbnails/{account_name}")
def get_simple_thumbnail_list(
    account_name: str,
    pages: Optional[int] = 3,
    date: Optional[str] = None,
    client: FacebookClient = Depends(FacebookClient),
) -> List[Dict[str, Union[str, AnyHttpUrl]]]:
    return client.get_thumbnail_list(account_name, pages=pages, date=date)
