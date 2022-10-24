import datetime
from pydantic import AnyHttpUrl, ValidationError

from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from facebook_scraper import get_posts
from dominate import document
from dominate.tags import div, img, h5

from app.config import Settings

settings = Settings()


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
        if pages > settings.max_facebook_pages:
            pages = settings.max_facebook_pages
        posts = list(get_posts(account, pages=pages))
        if date:
            dt = datetime.fromisoformat(date).date()
            posts = [post for post in posts if post['time'].date() == dt]
        return sorted(posts, key=lambda post: post['time'], reverse=True)

    def get_thumbnail_list(
        self,
        account: str,
        **kwargs
    ) -> List[Dict[str, Union[str, AnyHttpUrl]]]:
        """
        Get a simplified list posts with thumbnail, text and ID
        Args:
            account: name of account to to scrape
        """
        raw_posts = self.get_raw_posts(account, **kwargs)
        return [
            {
                'thumbnail': post['image'],
                'text': post['text'],
                'post_id': post['post_id'],
            }
            for post in raw_posts if post['image']
        ]

    def get_html_post(
        self,
        account: str,
        post_id: str,
        **kwargs,
    ):
        """
        Gets a rendered html document content for a given post_id and account_name
        Args:
            account: name of accout to scrape
            post_id: ID of post to display
        Returns:
            HTML content for post
        """
        thumbnail_posts = self.get_raw_posts(account, **kwargs)
        selected_post = next(
            (post for post in thumbnail_posts if post['post_id'] == post_id), None
        )
        return self.generate_single_post_html(selected_post) if selected_post else None

    @staticmethod
    def generate_single_post_html(post: Dict[str, Any]) -> str:
        """Generates a simple HTML document rendering thumbnail and post text"""
        # This should really be using templating
        doc = document(title=post['username'])
        with doc:
            with div():
                img(src=post['image'], style="width:150px;")
                h5(post['text'])
        return doc.render()
