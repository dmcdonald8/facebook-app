from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from pydantic import AnyHttpUrl
from services.facebook import FacebookClient

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/raw/{account_name}")
def get_raw_post_list(
    account_name: str,
    pages: Union[int, None] = 3,
    date: Union[str, None] = None,
    client: FacebookClient = Depends(FacebookClient),
) -> List[Dict[str, Any]]:
    """
    Fetch all Facebook posts for a given account name
    """
    return client.get_raw_posts(account_name, pages=pages, date=date)


@router.get("/thumbnails/{account_name}")
def get_thumbnail_post_list(
    account_name: str,
    pages: Optional[int] = 3,
    date: Optional[str] = None,
    client: FacebookClient = Depends(FacebookClient),
) -> List[Dict[str, Union[str, AnyHttpUrl]]]:
    """ Fetch a simplified list of posts keyed by thumbnail, text and post_id"""
    return client.get_thumbnail_list(account_name, pages=pages, date=date)


@router.get("/html/{account_name}/{post_id}", response_class=HTMLResponse)
def get_post_as_html(
    account_name: str,
    post_id: str,
    pages: Optional[int] = 3,
    date: Optional[str] = None,
    client: FacebookClient = Depends(FacebookClient),
) -> HTMLResponse:
    """ Get a simple HTML view of a single post """
    html_content = client.get_html_post(account_name, post_id, pages=pages, date=date)
    return HTMLResponse(content=html_content, status_code=200)
