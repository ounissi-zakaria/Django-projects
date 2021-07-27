from django.test import TestCase


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
