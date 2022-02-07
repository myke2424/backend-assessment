""" Client to interface with the hatchway blog posts API """

import concurrent.futures
import logging
from typing import List

import requests
from config import Config
from functools import cache
from .models import BlogPost
from .schemas import blog_post_schema

logger = logging.getLogger(__name__)
_GET_POST_URL = Config.HATCH_API_BLOG_POSTS_URL


@cache
def _get_blog_posts_with_tag_json(tag: str) -> List[dict]:
    """Get JSON response from GET request to blog posts api with the tag query param"""
    response = requests.get(_GET_POST_URL, params={"tag": tag}).json()
    return response


def _get_blog_posts_with_tag(tag: str) -> List[dict]:
    """Fetch all blog posts that the given tag"""
    posts = []
    posts_json = _get_blog_posts_with_tag_json(tag)

    for post in posts_json["posts"]:
        posts.append(blog_post_schema.load(post))

    return posts


def _get_blog_posts_for_all_tags(tags: List[str]) -> List[BlogPost]:
    """Fetch all blog posts for each tag in the list of tags."""
    all_posts = []

    for tag in tags:
        posts = _get_blog_posts_with_tag(tag=tag)
        for post in posts:
            all_posts.append(post)
    return all_posts


def _remove_duplicate_blog_posts(posts: List[BlogPost]) -> List[BlogPost]:
    """Remove all duplicate blog posts from a given list of blog posts"""
    post_ids = set()
    unique_posts = []
    for post in posts:
        if post.id not in post_ids:
            unique_posts.append(post)
        post_ids.add(post.id)
    return unique_posts


def get_unique_blog_posts_for_all_tags(tags: List[str]) -> List[BlogPost]:
    """Fetch all unique blog posts for each given tag (duplicate posts will be removed)"""
    posts = _get_blog_posts_for_all_tags(tags)
    unique_posts = _remove_duplicate_blog_posts(posts)
    logger.debug(f"Number of unique posts: {len(unique_posts)} for tags: {tags}")
    return unique_posts


def sort_blog_posts(posts: List[BlogPost], direction: str, sort_by: str) -> List[BlogPost]:
    """Sort the blog posts by a given key (sort_by) and direction ('asc' or 'desc')"""
    is_reverse = True if direction == "desc" else False
    return sorted(posts, key=lambda p: getattr(p, sort_by), reverse=is_reverse)


def serialize_blog_posts_to_json(posts: List[BlogPost]) -> dict:
    return {"posts": [post.to_json() for post in posts]}

#
#
# def get_posts_parallel(posts, url, tags):
#     """ Overhead of threads may not be worth if it's only a frew tags"""
#     if len(tags) > Config.SEQUENTIAL_REQUEST_LIMIT:
#         with concurrent.futures.ProcessPoolExecutor() as executor:
#             future_to_url = (executor.submit(_get_blog_posts_with_tag, url, tag) for
#                              tag in tags)
#             for future in concurrent.futures.as_completed(future_to_url):
#                 data = future.result()
#                 posts.append(data)


# def serialize_posts_to_json(posts: List[BlogPost]) -> dict:
#     return {"posts": [post.to_json() for post in posts]}
#
#
