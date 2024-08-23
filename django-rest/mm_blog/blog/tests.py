from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from .models import *

def login_with_default_user():
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


def create_post(client, data: dict):
    response = client.post("/api/blog/post/", data, format="json")
    assert response.status_code == 201

    response_data = response.json()

    return response_data

class PostViewTests(APITestCase):

    def test_post_view_return_status_200_for_authenticated_user(self):
        client = login_with_default_user()
        response = client.get("/api/blog/post/")

        self.assertEqual(response.status_code, 200, "Response status was not 200")

    def test_post_view_create_post(self):
        client = login_with_default_user()

        data = {
            "title": "This is title1",
            "text": "Description",
            "hashtags": ["test_hashtag1", "test_hashtag2"]
        }

        response_data = create_post(client, data)

        self.assertIsNotNone(response_data['pk'], "Primary key from the response was None")
        self.assertIsNotNone(response_data['created_at'], "created_at from the response was None")
        self.assertEqual(response_data['title'], data['title'], "Title was not matching")
        self.assertEqual([x['value'] for x in response_data['hashtags']], data['hashtags'], "Hashtags list was not equal")
        self.assertTrue(len(response_data['comment_set']) == 0, "Comments set was not empty")

    def test_update_existing_post(self):
        client = login_with_default_user()
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
        self.assertEqual(response.status_code, 200)

        response = client.get(f"/api/blog/post/{post_id}/", format="json")
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertEqual(response_data['pk'], post_id, "Returned post pk mismatch")
        self.assertEqual(response_data['title'], data['title'], "Updated title text mismatch")
        self.assertEqual(response_data['text'], data['text'], "Updated text mismatch")
        self.assertEqual([x['value'] for x in response_data['hashtags']], data['hashtags'], "Hashtags values does not match")

    
    def test_delete_post(self):
        client = login_with_default_user()
        data = {
            "title": "This is title1",
            "text": "Description",
            "hashtags": ["test_hashtag1", "test_hashtag2"]
        }

        response_data = create_post(client, data)
        post_id = response_data['pk']

        response = client.delete(f"/api/blog/post/{post_id}/")
        self.assertEqual(response.status_code, 204)

        response = client.get(f"/api/blog/post/{post_id}/", format="json")
        self.assertEqual(response.status_code, 404)



    def test_retriave_post_by_id_retruns_the_correct_post(self):
        client = login_with_default_user()
        data = {
            "title": "This is title1",
            "text": "Description",
            "hashtags": ["test_hashtag1", "test_hashtag2"]
        }

        response_data = create_post(client, data)
        post_id = response_data['pk']

        response = client.get(f"/api/blog/post/{post_id}/", format="json")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['pk'], post_id, "The post id does not match")


    def test_filter_posts_by_hashtags(self):
        client = login_with_default_user()
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
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertTrue(first_post_data['hashtags'][0] in [x['value'] for x in response_data['results'][0]['hashtags']])
        self.assertTrue(len(response_data['results']) == 1)


        response = client.get(f"/api/blog/post?hashtag={second_post_data['hashtags'][0]}", format="json", follow=True)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
 
        self.assertTrue(second_post_data['hashtags'][0] in [x['value'] for x in response_data['results'][0]['hashtags']])
        self.assertTrue(len(response_data['results']) == 1)


        response = client.get(f"/api/blog/post?hashtag={first_post_data['hashtags'][1]}", format="json", follow=True)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertTrue(first_post_data['hashtags'][1] and second_post_data['hashtags'][1] in [x['value'] for x in response_data['results'][0]['hashtags']])
        self.assertTrue(len(response_data['results']) == 2)

class CommentsTest(APITestCase):

    def test_create_comment(self):
        client = login_with_default_user()
        data = {
                "title": "This is title1",
                "text": "Description",
                "hashtags": ["second_hashtag", "test_hashtag2"]
            }

        post_data = create_post(client, data)

        comment_data = {
            "text": "Create new comment"
        }

        response = client.post(f"/api/blog/post/{post_data['pk']}/comments/", comment_data)

        self.assertEqual(response.status_code, 201)
        response_data = response.json()

        self.assertIsNotNone(response_data['pk'])
        self.assertEqual(response_data['text'], comment_data['text'])

    
    def test_delete_comment_by_id(self):
        client = login_with_default_user()
        data = {
                "title": "This is title1",
                "text": "Description",
                "hashtags": ["second_hashtag", "test_hashtag2"]
            }

        post_data = create_post(client, data)

        comment_data = {
            "text": "Create new comment"
        }

        response = client.post(f"/api/blog/post/{post_data['pk']}/comments/", comment_data, format="json")

        self.assertEqual(response.status_code, 201)
        response_data = response.json()

        response = client.delete(f"/api/blog/comment/{response_data['pk']}")
        self.assertEqual(response.status_code, 204)

        response = client.get(f"/api/blog/post/{post_data['pk']}/comments/", format="json")
        self.assertEqual(response.status_code, 200)

        respose_data = response.json()

        self.assertTrue(len(respose_data['results']) == 0)

    def test_update_comment(self):
        client = login_with_default_user()
        data = {
                "title": "This is title1",
                "text": "Description",
                "hashtags": ["second_hashtag", "test_hashtag2"]
            }

        post_data = create_post(client, data)

        comment_data = {
            "text": "Create new comment"
        }

        response = client.post(f"/api/blog/post/{post_data['pk']}/comments/", comment_data, format="json")
        comment_id = response.json()['pk']
        comment_data = {
            "text": "Update comment text"
        }

        response =  client.put(f"/api/blog/comment/{comment_id}", comment_data, format="json")

        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertEqual(response_data['pk'], comment_id)
        self.assertEqual(response_data['text'], comment_data['text'])


class HashtagTest(APITestCase):


    def test_delete_hashtag(self):
        
        client = login_with_default_user()
        data = {
                "title": "This is title1",
                "text": "Description",
                "hashtags": ["second_hashtag", "test_hashtag2"]
            }

        post_data = create_post(client, data)
        hashtag_id = post_data['hashtags'][0]['pk']
        response = client.delete(f"/api/blog/hashtag/{hashtag_id}")

        self.assertEqual(response.status_code, 204)

        response = client.get(f"/api/blog/post/{post_data['pk']}/", format="json")
        response_data = response.json()
        self.assertTrue(hashtag_id not in [x['value'] for x in response_data['hashtags']])