import random

from django.test.utils import setup_test_environment
from django.test import TestCase, Client
from django.urls import reverse

from .utils import Utils
from .models import *
import random


def login_with_default_user():
    client = Client()
    user = User.objects.create_user(username="test@test.com", password="test123")
    client.force_login(user)

    return client


def create_post(client, post_data: dict):
    return client.post(reverse("blog_post_app:post-home"), data=post_data)


def create_comment_to_blog_post(client):
    post_data = {
        "blog_post.title": "New Blog Post With Comment",
        "blog_post.text": "This is the content of the new blog post.",
        "hashtag_string": "#hashtag"
    }

    create_post(client, post_data)

    found_posts = BlogPost.objects.get(title="New Blog Post With Comment")
    comment_data = {
        "comment_text": "This is new comment"
    }

    return client.post(reverse("blog_post_app:post-comment", args=(found_posts.pk,)), data=comment_data), found_posts


def create_post_for_rating(client):
    post_data = {
        "blog_post.title": f"New Blog Post for rating Comment {random.randint(10000, 1000000)}",
        "blog_post.text": "This is the content of the new blog post.",
        "hashtag_string": "#hashtag"
    }

    create_post(client, post_data)

    return BlogPost.objects.get(title=post_data['blog_post.title'])


class BlogHomeTests(TestCase):

    def test_get_home_response_status_code_is_200(self):
        client = Client()
        response = client.get(reverse("blog_post_app:get-home"))

        self.assertEqual(response.status_code, 200, "Response status was not 200")

    def test_get_home_response_contains_all_context(self):
        client = Client()
        response = client.get(reverse("blog_post_app:get-home"))

        self.assertQuerySetEqual(response.context["blog_posts"], [])
        self.assertIsNotNone(response.context['blog_post'])
        self.assertIs(response.context['comment_text'].__class__, type(str()))
        self.assertIs(response.context['hashtag_string'].__class__, type(str()))

    def test_create_new_post(self):
        post_data = {
            "blog_post.title": "New Blog Post",
            "blog_post.text": "This is the content of the new blog post.",
            "hashtag_string": "#hashtag, #test"
        }

        client = login_with_default_user()
        response = create_post(client, post_data)

        self.assertEqual(response.status_code, 302)

        found_posts = BlogPost.objects.get(title="New Blog Post")
        hashtags = found_posts.hashtag_set.all()
        hashtag_values = [x.value for x in hashtags]

        self.assertIsNotNone(found_posts, "Found posts is None")
        self.assertEqual(found_posts.text, "This is the content of the new blog post.", "Text is not matching")
        self.assertTrue("#hashtag" in hashtag_values, "Hashtag is not in the query set")
        self.assertTrue("#test" in hashtag_values, "Hashtag is not in the query set")

    def test_newly_created_post_is_in_the_html_content(self):
        post_data = {
            "blog_post.title": "New Blog Post Html content",
            "blog_post.text": "This is the content of the new blog post.",
            "hashtag_string": "#hashtag, #test"
        }

        client = login_with_default_user()
        create_post(client, post_data)

        response = client.get(reverse("blog_post_app:get-home"))
        html_content_decoded = response.content.decode("utf-8")

        self.assertTrue(post_data['blog_post.title'] in html_content_decoded)
        self.assertTrue(post_data['blog_post.text'] in html_content_decoded)


class PostCommentTests(TestCase):

    def test_add_comment_to_a_post(self):
        client = login_with_default_user()
        response, blog_post = create_comment_to_blog_post(client)

        self.assertEqual(response.status_code, 302)

        comments = blog_post.comment_set.all()
        comments_text = [x.text for x in comments]

        self.assertTrue("This is new comment" in comments_text, "Comment text is not present in the post comments")

    def test_comment_owner_is_the_logged_user(self):
        client = login_with_default_user()
        response, blog_post = create_comment_to_blog_post(client)

        self.assertEqual(response.status_code, 302)

        comments = blog_post.comment_set.all()
        comments_usernames = [x.user.username for x in comments]

        self.assertTrue(response.wsgi_request.user.username in comments_usernames,
                        "Logged user username is not in the blog post comments response")


class PostRatingTests(TestCase):

    def test_positive_rating_on_post(self):
        client = login_with_default_user()
        blog_post = create_post_for_rating(client)
        initial_rating = blog_post.positive_rating
        response = client.post(reverse("blog_post_app:post-positive-rating", args=(blog_post.pk,)))

        blog_post = BlogPost.objects.get(title=blog_post.title)

        self.assertEqual(response.status_code, 302)
        self.assertIs(blog_post.positive_rating, initial_rating + 1, "Rating is not incremented by 1")

    def test_negative_rating_on_post(self):
        client = login_with_default_user()
        blog_post = create_post_for_rating(client)
        initial_rating = blog_post.positive_rating
        response = client.post(reverse("blog_post_app:post-negative-rating", args=(blog_post.pk,)))

        blog_post = BlogPost.objects.get(title=blog_post.title)

        self.assertEqual(response.status_code, 302)
        self.assertIs(blog_post.negative_rating, initial_rating + 1, "Rating is not incremented by 1")


class UtilityFunctionsTest(TestCase):

    def test_modify_hashtag_string(self):
        hashtag_string_unformatted = "#hashtag, #second_hashtag #third \
         #anotherone    last_one"

        hashtags = Utils.modify_hashtag_raw_string(hashtag_string_unformatted)
        self.assertIs(len(hashtags), 5)
