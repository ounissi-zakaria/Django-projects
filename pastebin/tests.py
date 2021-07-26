from django.test import TestCase, TransactionTestCase
from django.urls import reverse


class TextIndexViewTest(TransactionTestCase):
    def test_new_form(self):
        """
        Creating new valid form redirects to it's detail with the stored text.
        """
        text_body = "Text Test"
        response = self.client.post(
            "/pastebin/",
            data={"body": text_body},
        )
        self.assertEqual(response.status_code, 302)
        url = response.url
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text_body)

    def test_two_texts_with_same_body(self):
        """
        If text already exists client should be redirected but not create second instance of the text.
        """
        text_body = "Text Test"
        response = self.client.post(
            "/pastebin/",
            data={"body": text_body},
        )
        response = self.client.post(
            "/pastebin/",
            data={"body": text_body},
        )
        url = response.url
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text_body)
