from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth.models import User

# Create your tests here.


class UserTestCase(TestCase):

    def setUp(self):

        en_password = make_password('1234')
        User.objects.create(
            username='user1', password=en_password, email='user1@exp.com')
        User.objects.create(
            username='user2', password=en_password, email='user2@exp.com', is_superuser='False')
        User.objects.create(
            username='admin', password=en_password, email='admin@exp.com', is_superuser='True')

    def test_index_view(self):
        c = Client()
        responses = c.get(reverse('user:index'))
        self.assertEqual(responses.status_code, 200)

    def test_about_view(self):
        c = Client()
        responses = c.get(reverse('user:about'))
        self.assertEqual(responses.status_code, 200)

    def test_login_view(self):
        c = Client()
        responses = c.get(reverse('user:login'))
        self.assertEqual(responses.status_code, 200)


# login_check view

    def test_login_check_view_with_authen(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(reverse('user:login_check'))
        self.assertEqual(responses.status_code, 302)

    def test_login_check_view_without_authen_and_no_post(self):
        c = Client()
        responses = c.get(reverse('user:login_check'))
        self.assertEqual(responses.status_code, 200)

    def test_login_check_view_without_authen_and_can_authen(self):
        c = Client()
        responses = c.post(reverse('user:login_check'),
                           {'username': 'user1',
                            'password': '1234'
                            })
        self.assertEqual(responses.status_code, 302)

    def test_login_check_view_without_authen_and_can_not_authen(self):
        c = Client()
        responses = c.post(reverse('user:login_check'),
                           {'username': 'randomuser',
                            'password': '263514'
                            })
        self.assertEqual(responses.status_code, 302)


# confirm_register view

    def test_register_view_no_post(self):
        c = Client()
        responses = c.get(reverse('user:confirm_register'))
        self.assertEqual(responses.status_code, 200)

    def test_register_view_already_have_this_username(self):
        c = Client()
        responses = c.post(reverse('user:confirm_register'),
                           {'username': 'user1',
                            'password': '263514',
                            're_password': '263514',
                            'email': 'test@gmail.com',
                            'first_name': 'Hello',
                            'last_name': 'World',
                            })
        self.assertEqual(responses.status_code, 200)

    def test_cregister_view_invalid_password(self):
        c = Client()
        # Password must have at least 8
        c.post(reverse('user:confirm_register'),
               {'username': 'testuser',
                'password': '2',
                're_password': '2',
                'email': 'test@gmail.com',
                'first_name': 'Hello',
                'last_name': 'World',
                })
        # Password must have at least 1 of a-z
        c.post(reverse('user:confirm_register'),
               {'username': 'testuser',
                'password': '12345678',
                're_password': '12345678',
                'email': 'test@gmail.com',
                'first_name': 'Hello',
                'last_name': 'World',
                })
        # Password must have at least 1 of A-Z
        c.post(reverse('user:confirm_register'),
               {'username': 'testuser',
                'password': '12345678a',
                're_password': '12345678a',
                'email': 'test@gmail.com',
                'first_name': 'Hello',
                'last_name': 'World',
                })
        # Password must have at least 1 of 0-9
        c.post(reverse('user:confirm_register'),
               {'username': 'testtest',
                'password': 'dwadadsawsaASDSADW',
                're_password': 'dwadadsawsaASDSADW',
                'email': 'test@gmail.com',
                'first_name': 'Hello',
                'last_name': 'World',
                })
        # Invalid password confirm
        c.post(reverse('user:confirm_register'),
               {'username': 'testuser',
                'password': '12345asdWQDSA',
                're_password': '123456321',
                'email': 'test@gmail.com',
                'first_name': 'Hello',
                'last_name': 'World',
                })
        # This email is already taken
        c.post(reverse('user:confirm_register'),
               {'username': 'testuser',
                'password': '12345asdWQDSA',
                're_password': '12345asdWQDSA',
                'email': 'user1@exp.com',
                'first_name': 'Hello',
                'last_name': 'World',
                })
        # Can register
        c.post(reverse('user:confirm_register'),
               {'username': 'testuser',
                'password': '12345asdWQDSA',
                're_password': '12345asdWQDSA',
                'email': 'test@exp.com',
                'first_name': 'Hello',
                'last_name': 'World',
                })

# logout view
    def test_logout_view(self):
        c = Client()
        responses = c.get(reverse('user:logout'))
        self.assertEqual(responses.status_code, 302)


# register_view view

    def test_register_view_view(self):
        c = Client()
        responses = c.get(reverse('user:register'))
        self.assertEqual(responses.status_code, 200)

# admin_view view

    def test_admin_view_view_without_authen(self):
        c = Client()
        responses = c.get(reverse('user:admin'))
        self.assertEqual(responses.status_code, 302)

    def test_admin_view_view_without_superuser(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(reverse('user:admin'))
        self.assertEqual(responses.status_code, 302)

    def test_admin_view_view_with_superuser(self):
        c = Client()
        user = User.objects.get(username='admin', email='admin@exp.com')
        c.force_login(user)
        responses = c.get(reverse('user:admin'))
        self.assertEqual(responses.status_code, 200)


# my_profile view

    def test_my_profile_view_without_auth(self):
        c = Client()
        responses = c.get(reverse('user:my_profile'))
        self.assertEqual(responses.status_code, 302)

    def test_my_profile_view(self):
        c = Client()
        user = User.objects.get(username='admin', email='admin@exp.com')
        c.force_login(user)
        responses = c.get(reverse('user:my_profile'))
        self.assertEqual(responses.status_code, 200)


# update_profile view


    def test_update_profile_view_without_auth(self):
        c = Client()
        responses = c.get(reverse('user:update_profile'))
        self.assertEqual(responses.status_code, 302)

    def test_update_profile_view_with_post(self):
        c = Client()
        user = User.objects.get(username='admin', email='admin@exp.com')
        c.force_login(user)
        responses = c.post(reverse('user:update_profile'),
                           {'new_first_name': 'newfirstnameadmin',
                            'new_last_name': 'newlasnameadmin',
                            'new_email': 'newadmin@admin.com',
                            })
        self.assertEqual(responses.status_code, 302)

    def test_update_profile_view_without_post(self):
        c = Client()
        user = User.objects.get(username='admin')
        c.force_login(user)
        responses = c.get(reverse('user:update_profile'))
        self.assertEqual(responses.status_code, 200)


# change_password view


    def test_change_password_view_without_auth(self):
        c = Client()
        responses = c.get(reverse('user:change_password'))
        self.assertEqual(responses.status_code, 302)

    def test_change_password_view_with_post(self):
        c = Client()
        user = User.objects.get(username='user1')
        c.force_login(user)
        c.post(reverse('user:change_password'),
               {'old_password': '1234',
                'new_password': '1234AAAbbbcc',
                'new_re_password': '1234AAAbbbcc',
                })

    def test_change_password_view_with_post_newpassword_same_oldpassword(self):
        c = Client()
        user = User.objects.get(username='user1')
        c.force_login(user)
        c.post(reverse('user:change_password'),
               {'old_password': '1234',
                'new_password': '1234',
                'new_re_password': '1234AAAbbbcc',
                })

    def test_change_password_view_with_post_newpassword_length_more_than_eight(self):
        c = Client()
        user = User.objects.get(username='user1')
        c.force_login(user)
        c.post(reverse('user:change_password'),
               {'old_password': '1234',
                'new_password': '123412',
                'new_re_password': '1234AAAbbbcc',
                })

    def test_change_password_view_with_post_newpassword_need_atleast_one_a_to_z(self):
        c = Client()
        user = User.objects.get(username='user1')
        c.force_login(user)
        c.post(reverse('user:change_password'),
               {'old_password': '1234',
                'new_password': '1234122131',
                'new_re_password': '1234AAAbbbcc',
                })

    def test_change_password_view_with_post_newpassword_need_atleast_one_A_to_Z(self):
        c = Client()
        user = User.objects.get(username='user1')
        c.force_login(user)
        c.post(reverse('user:change_password'),
               {'old_password': '1234',
                'new_password': '1234122131a',
                'new_re_password': '1234AAAbbbcc',
                })

    def test_change_password_view_with_post_newpassword_need_atleast_one_zero_to_nine(self):
        c = Client()
        user = User.objects.get(username='user1')
        c.force_login(user)
        c.post(reverse('user:change_password'),
               {'old_password': '1234',
                'new_password': 'aaaazzzzzzAAA',
                'new_re_password': '1234AAAbbbcc',
                })

    def test_change_password_view_with_post_new_password_not_equal_new_re_password(self):
        c = Client()
        user = User.objects.get(username='user1')
        c.force_login(user)
        c.post(reverse('user:change_password'),
               {'old_password': '1234',
                'new_password': 'aaaazzzzzz11AAA',
                'new_re_password': '1234AAAbbbcc',
                })

    def test_change_password_view_with_post_wrong_old_password(self):
        c = Client()
        user = User.objects.get(username='user1')
        c.force_login(user)
        c.post(reverse('user:change_password'),
               {'old_password': '1234addaw',
                'new_password': 'aaaazzzzzz11AAA',
                'new_re_password': '1234AAAbbbcc',
                })

    def test_change_password_view_without_post(self):
        c = Client()
        user = User.objects.get(username='admin', email='admin@exp.com')
        c.force_login(user)
        responses = c.get(reverse('user:change_password'))
        self.assertEqual(responses.status_code, 200)
