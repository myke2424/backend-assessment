from marshmallow import Schema, fields, post_load, validate

from models import Post


class BlogPostSchema(Schema):
    id_ = fields.Int(data_key="id")
    author = fields.Str()
    author_id = fields.Int(data_key="authorId")
    likes = fields.Int()
    popularity = fields.Float()
    reads = fields.Int()
    tags = fields.List(fields.Str())

    @post_load
    def make_post(self, data: dict, **kwargs) -> Post:
        """Create the post object"""
        return Post(**data)


class BlogPostsRequestQueryParams(Schema):
    tags: fields.Str(required=True)
    sort_by: fields.Str(validate=validate.OneOf(['id', 'reads', 'likes', 'popularity']), missing='id')
    direction: fields.Str(validate=validate.OneOf(['asc', 'desc']), missing='asc')


blog_post_schema = BlogPostSchema()
blog_posts_request_query_params_schema = BlogPostsRequestQueryParams()
