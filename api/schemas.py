from marshmallow import Schema, fields, post_load, pre_load

from .errors import (InvalidDirectionParameterError,
                     InvalidSortByParameterError, QueryParamMissingError)
from .models import BlogPost


class BlogPostSchema(Schema):
    id = fields.Int()
    author = fields.Str()
    author_id = fields.Int(data_key="authorId")
    likes = fields.Int()
    popularity = fields.Float()
    reads = fields.Int()
    tags = fields.List(fields.Str())

    @post_load
    def make_post(self, data: dict, **kwargs) -> BlogPost:
        """Create the post object"""
        return BlogPost(**data)


class BlogPostsRequestQueryParams(Schema):
    tags = fields.Str()
    sort_by = fields.Str(missing="id")
    direction = fields.Str(missing="asc")

    @pre_load
    def _validate_params(self, data, **kwargs) -> None:
        """Validate query parameters"""
        if data.get("tags") is None:
            raise QueryParamMissingError("tags parameter is required")

        if data.get("sort_by") not in ("id", "reads", "likes", "popularity"):
            raise InvalidSortByParameterError(
                "sortBy parameter is invalid - must be one of the following: (id,reads, likes, popularity)"
            )

        if data.get("direction") not in ("asc", "desc"):
            raise InvalidDirectionParameterError(
                "direction parameter is invalid - must be of the following: (asc, desc)"
            )


blog_post_schema = BlogPostSchema()
blog_posts_request_query_params_schema = BlogPostsRequestQueryParams()
