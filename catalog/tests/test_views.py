from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls  import reverse
from catalog.models import Photo


def make_user():
    return User.objects.create_user(
        username = 'tester',
        email = 'tester@example.com',
        password = 'secret'
    )


class PhotoListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = make_user()
        user.save()
        for n in range(25):
            Photo.objects.create(
                author = user,
                tags = 'test image ' + str(n),
                photo = SimpleUploadedFile(
                    name = 'test_image.jpg',
                    content = open('catalog/tests/test_image.jpg', 'rb').read(),
                    content_type = 'image/jpeg'
                )
            )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/catalog/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalog/photo_list.html')

    def test_pagination_is_twenty(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['photo_list']) == 20)

    def test_lists_all_authors(self):
        resp = self.client.get(reverse('index')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['photo_list']) == 5)


class PhotoListByUserTest(TestCase):       

    @classmethod
    def setUpTestData(cls):
        user = make_user()
        for n in range(25):
            Photo.objects.create(
                author = user,
                tags = 'test image ' + str(n),
                photo = SimpleUploadedFile(
                    name = 'test_image.jpg',
                    content = open('catalog/tests/test_image.jpg', 'rb').read(),
                    content_type = 'image/jpeg'
                )
            )

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='tester', password='secret')
        resp = self.client.get('/catalog/myphotos/')
        self.assertEqual(str(resp.context['user']), 'tester')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='tester', password='secret')
        resp = self.client.get(reverse('by-user'))
        self.assertEqual(str(resp.context['user']), 'tester')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='tester', password='secret')
        resp = self.client.get(reverse('by-user'))
        self.assertEqual(str(resp.context['user']), 'tester')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalog/photo_by_user.html')

    def test_pagination_is_twenty(self):
        login = self.client.login(username='tester', password='secret')
        resp = self.client.get(reverse('by-user'))
        self.assertEqual(str(resp.context['user']), 'tester')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['photo_list']) == 20)

    def test_lists_all_authors(self):
        login = self.client.login(username='tester', password='secret')
        resp = self.client.get(reverse('by-user')+'?page=2')
        self.assertEqual(str(resp.context['user']), 'tester')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['photo_list']) == 5)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('by-user'))
        self.assertRedirects(resp, '/accounts/login/?next=/catalog/myphotos/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='tester', password='secret')
        resp = self.client.get(reverse('by-user'))
        self.assertEqual(str(resp.context['user']), 'tester')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalog/photo_by_user.html')

    def test_only_users_photos_in_list(self):
        login = self.client.login(username='tester', password='secret')
        resp = self.client.get(reverse('by-user'))
        self.assertEqual(str(resp.context['user']), 'tester')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('photo_list' in resp.context)
        self.assertEqual( len(resp.context['photo_list']) ,20)
        for photo in resp.context['photo_list']:
            self.assertEqual(resp.context['user'], photo.author)
