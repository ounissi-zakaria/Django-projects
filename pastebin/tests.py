from django.test import TestCase, TransactionTestCase
from django.urls import reverse

from .forms import TextForm


class TextIndexViewTests(TransactionTestCase):
    def test_new_text(self):
        """
        Creating new valid text redirects to it's detail with the stored body.
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


class TextFormTests(TestCase):
    def test_valid_form(self):
        """
        forms with valid text are valid.
        """
        text_body = "Text  Text"
        form = TextForm({"body": text_body})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Empty forms are not valid
        """
        text_body = ""
        form = TextForm({"body": text_body})
        self.assertFalse(form.is_valid())
