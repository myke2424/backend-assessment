import pytest
from app import app


@pytest.fixture
def client():
    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client


def test_ping(client):
    response = client.get('/api/ping')
    assert response.status_code == 200


def test_get_blog_posts(client):
    response = client.get('/api/posts?tags=science,tech')
    assert response.status_code == 200


def test_get_blog_posts_no_tags(client):
    response = client.get('/api/posts')
    assert response.status_code == 400


def test_get_blog_posts_invalid_sort_by_param(client):
    response = client.get('/api/posts?tags=science,tech&sortBy=apples')
    assert response.status_code == 400


def get_blog_posts_invalid_direction_param(client):
    response = client.get('/api/posts?tags=science,tech&direction=bananas')
    assert response.status_code == 400
