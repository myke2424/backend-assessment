import concurrent.futures
import logging
from functools import cache
from typing import List

import requests
from flask import Flask, request

from config import Config
from decorators import http_error_handler
from errors import QueryParamMissingError
from models import Post
from schemas import blog_post_schema

app = Flask(__name__)

logging.basicConfig(
    level=Config.LOG_LEVEL,
    format=Config.LOG_FORMAT,
    handlers=[logging.FileHandler(Config.LOG_FILE_PATH), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
logger.setLevel(Config.DEBUG)


@app.route("/api/ping", methods=["GET"])
def ping():
    """Endpoint to check the API is up and running!"""
    response = {"success": True}
    return response, 200


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
        if post.id_ not in post_ids:
            unique_posts.append(post)
        post_ids.add(post.id_)
    return unique_posts


def serialize_posts_to_json(posts: List[Post]) -> dict:
    return {"posts": [post.to_json() for post in posts]}


def sort_posts(posts: dict, direction: str, sort_by: str):
    order = None
    if direction == 'desc':
        order = True
    elif direction == 'asc':
        order = False
    else:
        raise ValueError
    return sorted(posts, key=lambda key: key[sort_by], reverse=True)


@app.route("/api/posts", methods=["GET"])
@http_error_handler
@cache
def blog_posts():
    """
    GET a list of blog posts via the hatchway API queried by the tags' parameter.

    Query Parameters:
        tags: str - Required
            A comma separated list of tags.
        sortBy: Optional[str] - Default='id'.
            The field to sort the posts by. The acceptable fields are: (id, reads, likes, popularity).
        direction: Optional[str] - Default='asc'
            The direction for sorting. The acceptable fields are (desc, asc).

    Returns:

    """
    query_params = request.args

    tags = query_params.get("tags")
    sort_by = query_params.get("sortBy", "id")
    direction = query_params.get("direction", "asc")

    if tags is None:
        raise QueryParamMissingError("Tags parameter is required")

    tags = tags.split(",")  # parse comma seperated list of tags into a list
    posts = get_blog_posts_for_all_tags(
        url=Config.HATCH_API_BLOG_POSTS_URL, tags=tags, sort_by=sort_by, direction=direction
    )

    serialized_posts = serialize_posts_to_json(posts)
    sort_posts(posts=serialized_posts, direction=direction, sort_by=sort_by)

    return serialized_posts, 200
