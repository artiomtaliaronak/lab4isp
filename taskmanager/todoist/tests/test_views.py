from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from todoist.models import Task
from todoist.forms import CreateTaskForm

class TaskAndUsersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="1234567890")
        self.first_task = Task.objects.create(
            id="12345",
            title="test task",
            content="test example"
        )


    def test_create_user(self):
        user_name = "testerUser"
        user = User.objects.create(username=user_name, password="1234567890")
        user_two = User.objects.get(id=user.id)
        self.assertTrue(user.username == user_name)
        self.assertTrue(user.username == user_two.username)


    def test_task_form_invalid(self):
        task_form = CreateTaskForm(data={
            'title': "test task",
            }
        )
        self.assertFalse(task_form.is_valid())

    def test_task_form_valid(self):
        task_form = CreateTaskForm(data={
            'title': 'task tester',
            'content': 'text',
            }
        )
        self.assertTrue(task_form.is_valid())
        self.assertTrue(isinstance(task_form.save(commit=False), Task))

    def test_task_form_add(self):
        task_form = CreateTaskForm(data={
            'title': 'task tester add',
            'content': 'text',
            }
        )
        task = task_form.save(commit=False)
        task.user_creator = self.user
        task.save()
        task_two = Task.objects.get(id=task.id)
        self.assertTrue(task.title == task_two.title)
        self.assertTrue(task_two.title == "task tester add")

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester_views', password='12345')
        self.user.save()
        self.first_task = Task.objects.create(
            id="90577",
            title="first task",
            content="test example",
        )
    
    def test_index(self):
        response = self.client.get(reverse(''))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_register(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_task_page_no_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_sign_up_post_valid(self):
        response = self.client.post(reverse('register'), {
            'username': 'testersignip',
            'password1': 'pass123456',
            'password2': 'pass123456'
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_sign_up_post_invalid(self):
        response = self.client.post(reverse('register'), {
            'username': 'testersignip',
            'password1': 'pass123456',
            'password2': 'pdfvdvfdnj'
            }
        )
        self.assertEqual(response.status_code, 200)




