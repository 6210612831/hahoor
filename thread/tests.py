from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth.models import User

from thread.models import Sub_thread, Thread
import user
import datetime
from django.utils import timezone
# Create your tests here.


class UserTestCase(TestCase):

    def setUp(self):

        en_password = make_password('1234')
        user = User.objects.create(
            username='user1', password=en_password, email='user1@exp.com')
        thread = Thread.objects.create(header="Santa", content="#MARKDOWN_THREAD", author=user,
                                       date=datetime.datetime.now(tz=timezone.utc), )
        sub_thread = Sub_thread.objects.create(
            replyto=thread, content="#MARKDOWN_REPLY", author=user, date=datetime.datetime.now(tz=timezone.utc))
        thread.reply.add(sub_thread)
        thread.save()
# index view

    def test_index_view_without_search(self):
        c = Client()
        responses = c.get(reverse('thread:index'))
        self.assertEqual(responses.status_code, 200)

    def test_index_view_with_search(self):
        c = Client()
        responses = c.post(reverse('thread:index'), {'search': 'Santa'})
        self.assertEqual(responses.status_code, 200)

    def test_index_view_with_search_but_cant_find(self):
        c = Client()
        responses = c.post(reverse('thread:index'), {'search': 'Twintown'})
        self.assertEqual(responses.status_code, 200)

# thread view

    def test_thread_view(self):
        c = Client()
        responses = c.get(reverse('thread:thread', args=(1,)))
        self.assertEqual(responses.status_code, 200)


# my_thread view


    def test_my_thread_view_without_authen(self):
        c = Client()
        responses = c.get(reverse('thread:my_thread'))
        self.assertEqual(responses.status_code, 302)

    def test_my_thread_view_with_authen(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(reverse('thread:my_thread'))
        self.assertEqual(responses.status_code, 200)

# create_thread view

    def test_create_thread_view_without_authen(self):
        c = Client()
        responses = c.get(reverse('thread:create_thread'))
        self.assertEqual(responses.status_code, 200)

    def test_create_thread_view_with_post_and_already_have_this_header(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.post(reverse('thread:create_thread'), {'header': 'Santa',
                                                             'Content': '## MARKDOWN CONTENT'})
        self.assertEqual(responses.status_code, 200)

    def test_create_thread_view_with_post(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.post(reverse('thread:create_thread'), {'header': 'HELLO WORLD',
                                                             'Content': '## MARKDOWN CONTENT'})
        self.assertEqual(responses.status_code, 302)

    def test_create_thread_view_without_post(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(reverse('thread:create_thread'))
        self.assertEqual(responses.status_code, 200)
