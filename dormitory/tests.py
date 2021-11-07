from django.test import Client, TestCase
from .forms import MarkdownForm
from dormitory.forms import MarkdownForm

# Create your tests here.
from .models import *
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.hashers import make_password
import datetime
from django.utils import timezone
from PIL import Image


class DormitoryTestCase(TestCase):

    def setUp(self):

        en_password = make_password('1234')
        user = User.objects.create(
            username='user1', password=en_password, email='user1@exp.com')
        User.objects.create(
            username='user2', password=en_password, email='user2@exp.com', is_superuser='False')
        User.objects.create(
            username='admin', password=en_password, email='admin@exp.com', is_superuser='True')
        dorm = Dormitory.objects.create(title='Santa', desc='desc',
                                        content='content', author=user, date=datetime.datetime.now(tz=timezone.utc), status=True)
        Review.objects.create(reviewto=dorm, stars=3, content="##MARKDOWN_CONTENT",
                              author=user, date=datetime.datetime.now(tz=timezone.utc))

    def test_index_view_without_authen(self):
        c = Client()
        responses = c.get(reverse('dormitory:index'))
        self.assertEqual(responses.status_code, 200)


# Dormitories_view

    def test_dormitories_view_without_search_keyword(self):
        c = Client()
        responses = c.get(reverse('dormitory:dormitories'))
        self.assertEqual(responses.status_code, 200)

    def test_dormitories_view_with_search_keyword(self):
        c = Client()
        response = c.post(reverse('dormitory:dormitories'),
                          {'search': 'Santa', })
        self.assertEqual(response.status_code, 200)

    def test_dormitories_view_with_search_keyword_not_found(self):
        c = Client()
        response = c.post(reverse('dormitory:dormitories'),
                          {'search': 'Twintown', })
        self.assertEqual(response.status_code, 200)

    def test_dormitory_view(self):
        c = Client()
        responses = c.get(reverse('dormitory:dormitory', args=("Santa",)))
        self.assertEqual(responses.status_code, 200)


# Create_dormitory_view


    def test_create_dormitory_view_without_authen(self):
        c = Client()
        responses = c.get(reverse('dormitory:create_dormitory'))
        self.assertEqual(responses.status_code, 302)

    def test_create_dormitory_view_when_already_have_this_dormitory(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)

        # Create test file
        f = open("file_to_upload.txt", "a")
        f.write("Now the test file has more content!")
        f.close()

        with open("file_to_upload.txt", "rb") as a_file:
            responses = c.post(reverse('dormitory:create_dormitory'),
                               {'title': 'Santa',
                                'desc': 'Santa',
                                'icon_d': a_file,
                                'Content': "### Hello world"
                                })

        self.assertEqual(responses.status_code, 200)

    def test_create_dormitory_view_when_no_post(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(reverse('dormitory:create_dormitory'))
        self.assertEqual(responses.status_code, 200)


# my_dormitory_view


    def test_my_dormitory_view_without_authn(self):
        c = Client()
        responses = c.get(reverse('dormitory:my_dormitory'))
        self.assertEqual(responses.status_code, 302)

    def test_my_dormitory_view_with_authn(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(reverse('dormitory:my_dormitory'))
        self.assertEqual(responses.status_code, 200)


# remove_dormitory_view


    def test_remove_dormitory_view_without_authn(self):
        c = Client()
        responses = c.get(reverse('dormitory:remove_dormitory', args=(1,)))
        self.assertEqual(responses.status_code, 302)

    def test_remove_dormitory_view_without_superuser(self):
        c = Client()
        user = User.objects.get(username='user2', email='user2@exp.com')
        c.force_login(user)
        responses = c.get(reverse('dormitory:remove_dormitory', args=(1,)))
        self.assertEqual(responses.status_code, 302)

    def test_remove_dormitory_view(self):
        c = Client()
        user = User.objects.get(username='admin', email='admin@exp.com')
        c.force_login(user)
        responses = c.get(reverse('dormitory:remove_dormitory', args=(1,)))
        self.assertEqual(responses.status_code, 302)


# change_status_dormitory_view


    def test_change_status_dormitory_view_without_authn(self):
        c = Client()
        responses = c.get(
            reverse('dormitory:change_status_dormitory', args=(1,)))
        self.assertEqual(responses.status_code, 302)

    def test_change_status_dormitory_view_without_superuser(self):
        c = Client()
        user = User.objects.get(username='user2', email='user2@exp.com')
        c.force_login(user)
        responses = c.get(
            reverse('dormitory:change_status_dormitory', args=(1,)))
        self.assertEqual(responses.status_code, 302)

    def test_change_status_dormitory_view(self):
        c = Client()
        user = User.objects.get(username='admin', email='admin@exp.com')
        c.force_login(user)
        responses = c.get(
            reverse('dormitory:change_status_dormitory', args=(1,)))
        self.assertEqual(responses.status_code, 302)

# Review_dormitory view

    def test_review_dormitory_view_without_authen(self):
        c = Client()
        responses = c.get(
            reverse('dormitory:review_dormitory', args=(1,)))
        self.assertEqual(responses.status_code, 302)

    def test_review_dormitory_view_without_post(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(
            reverse('dormitory:review_dormitory', args=(1,)))
        self.assertEqual(responses.status_code, 302)

    def test_review_dormitory_view(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.post(
            reverse('dormitory:review_dormitory', args=(1,)),
            {'stars': 2,
             'content': "### Hello world"
             })
        self.assertEqual(responses.status_code, 302)


# Report_review view

    def test_report_review_view_without_authen(self):
        c = Client()
        responses = c.get(
            reverse('dormitory:report_review', args=(1,)))
        self.assertEqual(responses.status_code, 302)

    def test_report_review_view(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(
            reverse('dormitory:report_review', args=(1,)))
        self.assertEqual(responses.status_code, 302)
