from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class HomePageTest(TestCase):
    def setup(self):
        self.response = self.client.get(reverse('book:home'))

    def test_view_url_home(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'book/home.html')

    def test_home_contains_our_body_text(self):
        self.assertContains(self.response, 'کتابها')

    def test_pagination_is_correct(self):
        self.assertTrue(self.response.context['is_paginated'] is True)