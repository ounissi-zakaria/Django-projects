from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Topic, Comment
import datetime


def create_topic(title, body, days=0):
    time = timezone.now() + datetime.timedelta(days)
    return Topic.objects.create(topic_title=title, topic_body=body, topic_date=time)


class TopicIndexViewTests(TestCase):
    def test_no_topics(self):
        """
        Show appropriate message if there are no topics.
        """
        response = self.client.get(reverse("blog:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no available topics")
        self.assertQuerysetEqual(response.context["topic_list"], [])

    def test_one_past_topic(self):
        """
        Topics with past topic_date are displayed
        """
        topic = create_topic(
            title="Hello, its me",
            body="I was wondering if after all these years youd like to meet",
            days=-1,
        )
        response = self.client.get(reverse("blog:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["topic_list"], [topic])
        self.assertContains(response, topic.topic_title)

    def test_one_future_topic(self):
        """
        Topics with future topic_date are not displayed.
        """
        topic = create_topic(
            title="Hello, its me",
            body="I was wondering if after all these years youd like to meet",
            days=1,
        )
        response = self.client.get(reverse("blog:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["topic_list"], [])

    def test_one_past_one_future_topic(self):
        """
        Topics with topic_date in the past are displayed and topics with topic_date in the future are not displayed.
        """
        topic = create_topic(
            title="Hello", body="I was wondering if after all ", days=-1
        )
        create_topic(title="Its me", body="these years youd like to meet", days=1)
        response = self.client.get(reverse("blog:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["topic_list"], [topic])
        self.assertContains(response, topic.topic_title)

    def test_multiple_topics(self):
        """
        Display multiple topics
        """
        topic1 = create_topic(
            title="Hello", body="I was wondering if after all ", days=-1
        )
        topic2 = create_topic(
            title="Its me", body="these years youd like to meet", days=-2
        )
        response = self.client.get(reverse("blog:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["topic_list"], [topic1, topic2])
        self.assertContains(response, topic1.topic_title)
        self.assertContains(response, topic2.topic_title)


class TopicDetailViewTest(TestCase):
    def test_past_topic(self):
        """
        Topics with topic_date in the past are displayed.
        """
        topic = create_topic(
            title="Hello", body="I was wondering if after all ", days=-1
        )
        response = self.client.get(reverse("blog:detail", args=(topic.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, topic.topic_title)
        self.assertContains(response, topic.topic_body)

    def test_future_topic(self):
        """
        Topics with topic_date in the future are not accessible.
        """
        topic = create_topic(
            title="Hello", body="I was wondering if after all ", days=1
        )
        response = self.client.get(reverse("blog:detail", args=(topic.id,)))
        self.assertEqual(response.status_code, 404)


class CommentViewTest(TestCase):
    def test_topic_with_one_comment(self):
        """
        Topics with one comment show one comment.
        """
        topic = create_topic("lorem", "lorem ipsum")
        self.client.post(
            reverse("blog:detail", args=(topic.id,)),
            data={"user": "User1", "body": "Body1 Body1"},
        )
        response = self.client.get(reverse("blog:detail", args=(topic.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User1")
        self.assertContains(response, "Body1 Body1")

    def test_topic_with_multiple_comment(self):
        """
        Topics with multiple comments show multiple comments.
        """
        topic = create_topic("lorem", "lorem ipsum")
        self.client.post(
            reverse("blog:detail", args=(topic.id,)),
            data={"user": "User1", "body": "Body1 Body1"},
        )
        self.client.post(
            reverse("blog:detail", args=(topic.id,)),
            data={"user": "User2", "body": "Body2 Body2"},
        )
        response = self.client.get(reverse("blog:detail", args=(topic.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User1")
        self.assertContains(response, "Body1 Body1")
        self.assertContains(response, "User2")
        self.assertContains(response, "Body2 Body2")

    def test_comment_with_no_name(self):
        """
        Comments with no username are not registered.
        """
        topic = create_topic("lorem", "lorem ipsum")
        response = self.client.post(
            reverse("blog:detail", args=(topic.id,)),
            data={"user": "", "body": "Body1 Body1"},
        )
        self.assertEqual(response.status_code, 400)
        response = self.client.get(reverse("blog:detail", args=(topic.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["topic"].comment_set.all(), [])

    def test_comment_with_no_body(self):
        """
        Comments with no body are not registered.
        """
        topic = create_topic("lorem", "lorem ipsum")
        response = self.client.post(
            reverse("blog:detail", args=(topic.id,)),
            data={"user": "132", "body": ""},
        )
        self.assertEqual(response.status_code, 400)
        response = self.client.get(reverse("blog:detail", args=(topic.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["topic"].comment_set.all(), [])
