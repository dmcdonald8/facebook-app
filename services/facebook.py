import datetime
from pydantic import AnyHttpUrl

from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from facebook_scraper import get_posts


class FacebookClient:
    """ Client for scraping Facebook """

    def get_raw_posts(
        self,
        account: str,
        pages: int = 3,
        date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Gets list of posts in their raw format including all info ordered by
         date published and optionally filtered by date

        Args:
            account: name of the facebook account to scrape
            pages: number of facebook pages to scrape
            date: Optional[str] = None

        Returns:
            A list of ordered posts
        """
        posts = list(get_posts(account, pages=pages))
        if date:
            dt = datetime.fromisoformat(date).date()
            posts = [post for post in posts if post['time'].date() == dt]
        return sorted(posts, key=lambda post: post['time'], reverse=True)

    def get_thumbnail_list(
        self,
        account: str,
        pages: int = 3,
        date: Optional[str] = None
    ) -> List[Dict[str, Union[str, AnyHttpUrl]]]:
        raw_posts = self.get_raw_posts(account, pages=pages, date=date)
        return [
            {'thumbnail': post['image'], 'text': post['text']}
            for post in raw_posts if post['image']
        ]
