from rest_framework.test import APIClient
import pytest

from blog.models import *


@pytest.mark.django_db
def auth_client():
    client = APIClient()

    default_user = {
        "username": "admin",
        "email": "admin@email.com",
        "password": "test123",
        "is_staff": True    
    }

    response = client.post('/api/auth/signup', default_user, format="json")
    assert response.status_code, 201
    user = User.objects.get(email="admin@email.com")
    client.force_authenticate(user)

    return client


@pytest.mark.django_db
def create_post(client, data: dict):
    response = client.post("/api/blog/post/", data, format="json")
    assert response.status_code == 201

    response_data = response.json()

    return response_data



@pytest.mark.django_db
def test_post_view_return_status_200_for_authenticated_user():
    client = auth_client()
    response = client.get("/api/blog/post/")

    assert response.status_code == 200, "Response status was not 200"


@pytest.mark.django_db
def test_post_view_create_post():
    client = auth_client()

    data = {
        "title": "This is title1",
        "text": "Description",
        "hashtags": ["test_hashtag1", "test_hashtag2"]
    }

    response_data = create_post(client, data)

    assert response_data['pk'] != None, "Primary key from the response was None"
    assert response_data['created_at'] != None, "created_at from the response was None"
    assert response_data['title'] == data['title'], "Title was not matching"
    assert [x['value'] for x in response_data['hashtags']] == data['hashtags'], "Hashtags list was not equal"
    assert len(response_data['comments']) == 0, "Comments set was not empty"


@pytest.mark.django_db
def test_update_existing_post():
    client = auth_client()
    data = {
        "title": "This is title1",
        "text": "Description",
        "hashtags": ["test_hashtag1", "test_hashtag2"]
    }

    response_data = create_post(client, data)

    post_id = response_data['pk']

    data = {
        "title": "This is updated title1",
        "text": "Description update",
        "hashtags": ["test_hashtag1_update", "test_hashtag2_update"]
    }

    response = client.put(f"/api/blog/post/{post_id}/", data, format="json")
    assert response.status_code == 200

    response = client.get(f"/api/blog/post/{post_id}/", format="json")
    assert response.status_code == 200

    response_data = response.json()

    assert response_data['pk'] == post_id, "Returned post pk mismatch"
    assert response_data['title'] == data['title'], "Updated title text mismatch"
    assert response_data['text'] == data['text'], "Updated text mismatch"
    assert [x['value'] for x in response_data['hashtags']] == data['hashtags'], "Hashtags values does not match"

@pytest.mark.django_db
def test_delete_post():
    client = auth_client()
    data = {
        "title": "This is title1",
        "text": "Description",
        "hashtags": ["test_hashtag1", "test_hashtag2"]
    }

    response_data = create_post(client, data)
    post_id = response_data['pk']

    response = client.delete(f"/api/blog/post/{post_id}/")
    assert response.status_code == 204

    response = client.get(f"/api/blog/post/{post_id}/", format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_retriave_post_by_id_retruns_the_correct_post():
    client = auth_client()
    data = {
        "title": "This is title1",
        "text": "Description",
        "hashtags": ["test_hashtag1", "test_hashtag2"]
    }

    response_data = create_post(client, data)
    post_id = response_data['pk']

    response = client.get(f"/api/blog/post/{post_id}/", format="json")
    assert response.status_code == 200

    data = response.json()

    assert data['pk'] == post_id, "The post id does not match"

@pytest.mark.django_db
def test_filter_posts_by_hashtags():
    client = auth_client()
    first_post_data = {
        "title": "This is title1",
        "text": "Description",
        "hashtags": ["first_hashtag", "test_hashtag2"]
    }

    create_post(client, first_post_data)
    
    second_post_data = {
        "title": "This is title1",
        "text": "Description",
        "hashtags": ["second_hashtag", "test_hashtag2"]
    }

    create_post(client, second_post_data)

    response = client.get(f"/api/blog/post?hashtag={first_post_data['hashtags'][0]}", format="json", follow=True)
    assert response.status_code == 200

    response_data = response.json()

    assert first_post_data['hashtags'][0] in [x['value'] for x in response_data['results'][0]['hashtags']]
    assert len(response_data['results']) == 1


    response = client.get(f"/api/blog/post?hashtag={second_post_data['hashtags'][0]}", format="json", follow=True)
    assert response.status_code == 200

    response_data = response.json()

    assert second_post_data['hashtags'][0] in [x['value'] for x in response_data['results'][0]['hashtags']]
    assert len(response_data['results']) == 1


    response = client.get(f"/api/blog/post?hashtag={first_post_data['hashtags'][1]}", format="json", follow=True)
    assert response.status_code == 200

    response_data = response.json()

    assert first_post_data['hashtags'][1] and second_post_data['hashtags'][1] in [x['value'] for x in response_data['results'][0]['hashtags']]
    assert len(response_data['results']) == 2


@pytest.mark.django_db
def test_create_comment():
    client = auth_client()
    data = {
            "title": "This is title1",
            "text": "Description",
            "hashtags": ["second_hashtag", "test_hashtag2"]
        }

    post_data = create_post(client, data)

    comment_data = {
        "text": "Create new comment"
    }

    response = client.patch(f"/api/blog/post/{post_data['pk']}/add_comment/", comment_data)

    assert response.status_code == 201
    response_data = response.json()

    assert response_data['pk'] is not None
    assert response_data['text'] == comment_data['text']

@pytest.mark.django_db
def test_delete_comment_by_id():
    client = auth_client()
    data = {
            "title": "This is title1",
            "text": "Description",
            "hashtags": ["second_hashtag", "test_hashtag2"]
        }

    post_data = create_post(client, data)

    comment_data = {
        "text": "Create new comment"
    }

    response = client.patch(f"/api/blog/post/{post_data['pk']}/add_comment/", comment_data, format="json")

    assert response.status_code == 201
    response_data = response.json()

    response = client.delete(f"/api/blog/comment/{response_data['pk']}")
    assert response.status_code == 204

    response = client.get(f"/api/blog/post/{post_data['pk']}/comments/", format="json")
    assert response.status_code == 200

    respose_data = response.json()

    assert len(respose_data['results']) == 0


@pytest.mark.django_db
def test_update_comment():
    client = auth_client()
    data = {
            "title": "This is title1",
            "text": "Description",
            "hashtags": ["second_hashtag", "test_hashtag2"]
        }

    post_data = create_post(client, data)

    comment_data = {
        "text": "Create new comment"
    }

    response = client.patch(f"/api/blog/post/{post_data['pk']}/add_comment/", comment_data, format="json")
    comment_id = response.json()['pk']
    comment_data = {
        "text": "Update comment text"
    }

    response =  client.put(f"/api/blog/comment/{comment_id}", comment_data, format="json")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data['pk'] == comment_id
    assert response_data['text'] == comment_data['text']

@pytest.mark.django_db
def test_delete_hashtag():
    
    client = auth_client()
    data = {
            "title": "This is title1",
            "text": "Description",
            "hashtags": ["second_hashtag", "test_hashtag2"]
        }

    post_data = create_post(client, data)
    hashtag_id = post_data['hashtags'][0]['pk']
    response = client.delete(f"/api/blog/hashtag/{hashtag_id}")

    assert response.status_code == 204

    response = client.get(f"/api/blog/post/{post_data['pk']}/", format="json")
    response_data = response.json()
    assert hashtag_id not in [x['value'] for x in response_data['hashtags']]