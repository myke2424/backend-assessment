import logging
from http import HTTPStatus
from flask import Blueprint, request

from .decorators import http_error_handler
from .posts_client import (get_unique_blog_posts_for_all_tags,
                           serialize_blog_posts_to_json, sort_blog_posts)
from .schemas import blog_posts_request_query_params_schema

posts_api = Blueprint("api", __name__)

logger = logging.getLogger(__name__)


@posts_api.route("/ping", methods=["GET"])
def ping():
    """Endpoint to check the API is up and running!"""
    response = {"success": True}
    return response, 200


@posts_api.route("/posts", methods=["GET"])
@http_error_handler
def blog_posts():
    """
    Get a list of blog posts via the hatchway API.

    Query Parameters:
        tags: str - Required
            A comma separated list of tags.
        sortBy: Optional[str] - Default='id'.
            The field to sort the posts by. The acceptable fields are: (id, reads, likes, popularity).
        direction: Optional[str] - Default='asc'
            The direction for sorting. The acceptable fields are (desc, asc).

    Returns: JSON response of blog posts
    """

    query_params = request.args

    tags = query_params.get("tags")
    sort_by = query_params.get("sortBy", "id")
    direction = query_params.get("direction", "asc")

    blog_posts_request_query_params_schema.validate({"tags": tags, "sort_by": sort_by, "direction": direction})
    tags = tags.split(",")  # parse comma seperated list of tags into a list
    posts = sort_blog_posts(posts=get_unique_blog_posts_for_all_tags(tags), direction=direction, sort_by=sort_by)

    response = serialize_blog_posts_to_json(posts), HTTPStatus.OK
    return response
