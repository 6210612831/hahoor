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
        User.objects.create(
            username='user2', password=en_password, email='user2@exp.com')
        thread = Thread.objects.create(header="Santa", content="#MARKDOWN_THREAD", author=user,
                                       date=datetime.datetime.now(tz=timezone.utc), )
        sub_thread = Sub_thread.objects.create(
            replyto=thread, content="#MARKDOWN_REPLY", author=user, date=datetime.datetime.now(tz=timezone.utc))
        thread.reply.add(sub_thread)
        thread.id = 1
        thread.save()
        sub_thread.id = 1
        sub_thread.save()
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

    def test_thread_view_check_my_thread(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
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
        self.assertEqual(responses.status_code, 302)

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


# Update_thread view

    def test_update_thread_view_check_not_my_thread(self):
        c = Client()
        user = User.objects.get(username='user2', email='user2@exp.com')
        c.force_login(user)
        responses = c.get(reverse('thread:update_thread', args=(1,)))
        self.assertEqual(responses.status_code, 302)

    def test_update_thread_view_with_post(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.post(reverse('thread:update_thread', args=(1,)),
                           {'header': 'header',
                            'content': 'content'})
        self.assertEqual(responses.status_code, 302)

    def test_update_thread_view_without_post(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(reverse('thread:update_thread', args=(1,)))
        self.assertEqual(responses.status_code, 200)


# Reply_thread view

    def test_reply_thread_view_without_authen(self):
        c = Client()
        responses = c.get(reverse('thread:reply_thread', args=(1,)))
        self.assertEqual(responses.status_code, 302)

    def test_reply_thread_view_with_post(self):
        c = Client()
        user = User.objects.get(username='user2', email='user2@exp.com')
        c.force_login(user)
        responses = c.post(reverse('thread:reply_thread', args=(1,)),
                           {'content': 'content'})
        self.assertEqual(responses.status_code, 302)

    def test_reply_thread_view_without_post(self):
        c = Client()
        user = User.objects.get(username='user2', email='user2@exp.com')
        c.force_login(user)
        responses = c.get(reverse('thread:reply_thread', args=(1,)))
        self.assertEqual(responses.status_code, 302)


# Report_thread view

    def test_report_thread_view_without_authen(self):
        c = Client()
        responses = c.get(reverse('thread:report_thread', args=(1,)))
        self.assertEqual(responses.status_code, 302)

    def test_report_thread_view(self):
        c = Client()
        user = User.objects.get(username='user2', email='user2@exp.com')
        c.force_login(user)
        responses = c.get(reverse('thread:report_thread', args=(1,)))
        self.assertEqual(responses.status_code, 302)


# Report_subthread view


    def test_report_subthread_view_without_authen(self):
        c = Client()
        responses = c.get(reverse('thread:report_subthread', args=(1, 1,)))
        self.assertEqual(responses.status_code, 302)

    def test_report_subthread_view(self):
        c = Client()
        user = User.objects.get(username='user2', email='user2@exp.com')
        c.force_login(user)
        responses = c.get(reverse('thread:report_subthread', args=(1, 1,)))
        self.assertEqual(responses.status_code, 302)
