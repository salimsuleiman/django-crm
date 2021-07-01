from django.test import TestCase


class HomePageTest(TestCase):

    def test_status_code(self):
        res = self.client.get('/')
        print(res.content)
