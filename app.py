import logging
from functools import cache

from flask import Flask, request

from config import Config
from decorators import http_error_handler
from posts import (get_blog_posts_for_all_tags, serialize_posts_to_json,
                   sort_posts)
from schemas import blog_posts_request_query_params_schema

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

    blog_posts_request_query_params_schema.validate({"tags": tags, "sort_by": sort_by, direction: "direction"})
    tags = tags.split(",")  # parse comma seperated list of tags into a list

    posts = get_blog_posts_for_all_tags(url=Config.HATCH_API_BLOG_POSTS_URL, tags=tags)
    sorted_posts = sort_posts(posts=posts, direction=direction, sort_by=sort_by)

    response = serialize_posts_to_json(sorted_posts), 200

    return response
