from django.test import TestCase


class IconStudioPageTests(TestCase):
    def test_homepage_renders_icon_studio(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Field Kit")
        self.assertContains(response, 'data-icon="phone"')
        self.assertContains(response, "DOWNLOAD PNG")
