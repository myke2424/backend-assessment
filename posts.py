import logging
from typing import List

import requests

from models import Post
from schemas import blog_post_schema

logger = logging(__name__)


def _get_blog_posts_with_tag(url: str, tag: str) -> List[dict]:
    """
    Get all blog post for the tag.
    """
    query_params = {"tag": tag}
    response = requests.get(url, params=query_params)
    return response.json()


def get_blog_posts_for_all_tags(url: str, tags: List[str]) -> List[Post]:
    """get all blog posts for all tags"""
    all_posts = []

    for tag in tags:
        posts = _get_blog_posts_with_tag(url=url, tag=tag)
        for post in posts["posts"]:
            all_posts.append(blog_post_schema.load(post))
    unique_posts = _remove_duplicate_posts(all_posts)
    logger.debug(f"Number of unique posts: {len(unique_posts)} for tags: {tags}")

    return unique_posts


def _remove_duplicate_posts(posts: List[Post]) -> List[Post]:
    post_ids = set()
    unique_posts = []
    for post in posts:
        if post.id not in post_ids:
            unique_posts.append(post)
        post_ids.add(post.id)
    return unique_posts


def serialize_posts_to_json(posts: List[Post]) -> dict:
    return {"posts": [post.to_json() for post in posts]}


def sort_posts(posts: List[Post], direction: str, sort_by: str) -> List[Post]:
    is_reverse = True if direction == "desc" else False
    return sorted(posts, key=lambda p: getattr(p, sort_by), reverse=is_reverse)
