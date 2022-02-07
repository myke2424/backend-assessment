class Config:
    DEBUG = True
    PORT = 5000
    HOST = "127.0.0.1"
    JSON_SORT_KEYS = False
    LOG_LEVEL = "DEBUG"
    LOG_FORMAT = f"%(asctime)s %(levelname)s %(message)s"
    LOG_FILE_PATH = "api.log"
    HATCH_API_BLOG_POSTS_URL = "https://api.hatchways.io/assessment/blog/posts"
    SEQUENTIAL_REQUEST_LIMIT = 100
