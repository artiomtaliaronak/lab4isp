from django.test import SimpleTestCase
from django.urls import reverse, resolve
from todoist.views import createTask, viewTasks, login, register, profileManager

class TestUrls(SimpleTestCase):
    
    def test_createtask_url_is_resolved(self):
        url = reverse('createtask')
        self.assertEquals(resolve(url).func, createTask)

    def test_viewtasks_url_is_resolved(self):
        url = reverse('viewtasks')
        self.assertEquals(resolve(url).func, viewTasks)

    def test_profilemanager_url_is_resolved(self):
        url = reverse('profilemanager')
        self.assertEquals(resolve(url).func, profileManager)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login)

    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)


    
