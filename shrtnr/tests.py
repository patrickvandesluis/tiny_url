from django.test import TestCase, override_settings
from captcha.conf import settings as captcha_settings
from .models import Link


@override_settings(SECURE_SSL_REDIRECT=False)
class ShortenerTests(TestCase):
    def setUp(self):
        captcha_settings.CAPTCHA_TEST_MODE = True

    def post(self, link, short=''):
        return self.client.post('/', {
            'link': link,
            'short': short,
            'captcha_0': 'x',
            'captcha_1': 'PASSED',
        })

    def test_create_random_short(self):
        response = self.post('example.com/page')
        self.assertEqual(response.status_code, 200)
        link = Link.objects.get()
        self.assertEqual(link.link, 'https://example.com/page')
        self.assertRegex(link.short, r'^[a-z0-9]{8}$')

    def test_custom_short_is_lowercased(self):
        self.post('https://example.com', 'MyLink')
        self.assertTrue(Link.objects.filter(short='mylink').exists())

    def test_duplicate_short_any_case_is_rejected(self):
        Link.objects.create(link='https://example.com', short='abc')
        response = self.post('https://example.org', 'ABC')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Link.objects.count(), 1)
        self.assertContains(response, 'Short already exists')

    def test_invalid_short_is_rejected(self):
        for short in ['a b', 'x onfocus=alert(1)', 'a/b', 'admin', 'x' * 51]:
            self.post('https://example.com', short)
        self.assertEqual(Link.objects.count(), 0)

    def test_non_http_scheme_is_rejected(self):
        for link in ['javascript:alert(1)', 'ftp://example.com', 'data:text/html,hi']:
            self.post(link)
        self.assertEqual(Link.objects.count(), 0)

    def test_captcha_required(self):
        self.client.post('/', {'link': 'https://example.com', 'captcha_0': 'x', 'captcha_1': 'wrong'})
        self.assertEqual(Link.objects.count(), 0)

    def test_short_url_attribute_is_quoted(self):
        response = self.post('https://example.com', 'quoted')
        self.assertContains(response, 'value="https://vandesluis.com/quoted"')

    def test_redirect_counts_usage(self):
        Link.objects.create(link='https://example.com', short='abc')
        response = self.client.get('/abc')
        self.assertRedirects(response, 'https://example.com', fetch_redirect_response=False)
        self.assertEqual(Link.objects.get().times_used, 1)

    def test_unknown_short_goes_home(self):
        response = self.client.get('/nope')
        self.assertRedirects(response, '/', fetch_redirect_response=False)

    def test_ip_comes_from_x_real_ip(self):
        self.client.post('/', {
            'link': 'https://example.com', 'captcha_0': 'x', 'captcha_1': 'PASSED',
        }, HTTP_X_REAL_IP='203.0.113.5', HTTP_X_FORWARDED_FOR='1.2.3.4')
        self.assertEqual(Link.objects.get().ip, '203.0.113.5')
