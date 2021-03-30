
from django.test import SimpleTestCase #used when we do not need any database data
from django.urls import resolve,reverse
from MainApp.views import MainPage, register, ProfilePage, ProfileSettings, ProfileFollowing, ProfileFollowers
from django.contrib.auth import views as auth_views

class TestUrls(SimpleTestCase):

    def test_homepage_url_resolves(self):
        url = reverse('MainApp:homepage')
        #Make sure no a the homepage url mapes to MainPage
        self.assertEquals(resolve(url).func.view_class, MainPage)

    def test_register_url_resolves(self):
        url = reverse('MainApp:register')
        #Make sure no a the homepage url mapes to MainPage
        self.assertEquals(resolve(url).func, register)

    def test_login_url_resolves(self):
        url = reverse('MainApp:login')
        #Make sure no a the homepage url mapes to MainPage
        self.assertEquals(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_url_resolves(self):
        url = reverse('MainApp:logout')
        #Make sure no a the homepage url mapes to MainPage
        self.assertEquals(resolve(url).func.view_class, auth_views.LogoutView)

    def test_profile_url_resolves(self):
        #Test to see if we can reach the profile page view with the profile 'some-user'
        url = reverse('MainApp:profile',args=['some-user'])
        #Make sure no a the homepage url mapes to MainPage
        self.assertEquals(resolve(url).func.view_class, ProfilePage)
    
    def test_profile_settings_url_resolves(self):
        #Test to see if we can reach the profile page view with the profile 'some-user'
        url = reverse('MainApp:settingstab',args=['some-user'])
        #Make sure no a the homepage url mapes to MainPage
        self.assertEquals(resolve(url).func.view_class, ProfileSettings)

    def test_profile_followingtab_url_resolves(self):
        #Test to see if we can reach the profile page view with the profile 'some-user'
        url = reverse('MainApp:followingtab',args=['some-user'])
        #Make sure no a the homepage url mapes to MainPage
        self.assertEquals(resolve(url).func.view_class, ProfileFollowing)

    def test_profile_followerstab_url_resolves(self):
        #Test to see if we can reach the profile page view with the profile 'some-user'
        url = reverse('MainApp:followerstab',args=['some-user'])
        #Make sure no a the homepage url mapes to MainPage
        self.assertEquals(resolve(url).func.view_class, ProfileFollowers)
    
    
    
    