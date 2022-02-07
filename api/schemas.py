from marshmallow import Schema, fields, post_load, pre_load, validate

from .errors import QueryParamMissingError
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
    tags: fields.Str()
    sort_by: fields.Str(validate=validate.OneOf(["id", "reads", "likes", "popularity"]), missing="id")
    direction: fields.Str(validate=validate.OneOf(["asc", "desc"]), missing="asc")

    @pre_load
    def validate_tags(self, data, **kwargs) -> None:
        """Validate if tags are in query params"""
        if data.get("tags") is None:
            raise QueryParamMissingError("Tags parameter is required")


blog_post_schema = BlogPostSchema()
blog_posts_request_query_params_schema = BlogPostsRequestQueryParams()
