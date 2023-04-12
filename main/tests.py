from django.test import TestCase

from main.models import SiteLinks


class SingletonTest(TestCase):
    def setUp(self):
        self.links = SiteLinks()
        self.links.save()

    def tearDown(self):
        self.links.delete()

    def test_sameness(self):
        print("\nMethod: test_sameness")
        new_links = SiteLinks(telegram='telegram')
        new_links.save()
        self.assertEqual(self.links, new_links)
