from django.test import TestCase
from django.urls import reverse

from .models import Task


class IndexViewTest(TestCase):
    def test_no_task(self):
        """
        if there are no tasks show the appropriate message.
        """
        response = self.client.get("/todo/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no tasks")

    def test_valid_post_task(self):
        """
        Posting a valid task should refresh and display the task added.
        """
        task_body = "Task Text Text"
        response = self.client.post("/todo/", data={"body": task_body})
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/todo/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, task_body)

    def test_invalid_post_task(self):
        """
        Empty invalid post requests shouldn't register new tasks
        """
        task_body = ""
        response = self.client.post("/todo/", data={"body": task_body})
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/todo/")
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["task_list"], [])


class DeleteViewTest(TestCase):
    def test_delete_element(self):
        """
        Deleted elements are removed from the DateBase and are no longer displayed.
        """
        task_body = "Task Text Text"
        task = Task.objects.create(body=task_body)
        response = self.client.post(reverse("todo:delete", args=(task.id,)))
        self.assertEqual(response.status_code, 302)

        response = self.client.get("/todo/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no tasks")

    def test_delete_element_twice(self):
        """
        Server should return 404 error if element doesn't exist.
        """
        task_body = "Task Text Text"
        task = Task.objects.create(body=task_body)
        task_id = task.id
        self.client.post(reverse("todo:delete", args=(task_id,)))
        response = self.client.post(reverse("todo:delete", args=(task_id,)))
        self.assertEqual(response.status_code, 404)
