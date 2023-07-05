from django.contrib.auth.views import LoginView
from django.urls import path

LoginView
from .views import (
    get_cookie_view,
    set_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
    AboutMeView,
    RegisterView,
    FooBarView,
    add_avatar,
    AllUsersListView,
    UserDetailsView,
    update_avatar,
    HelloView,
)

app_name = "myauth"
urlpatterns = [
    # path("login/", login_view, name="login"),
    path("login/",
         LoginView.as_view(
             template_name="myauth/login.html",
             redirect_authenticated_user=True),
         name="login"
         ),
    path("hello/", HelloView.as_view(), name="hello"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("about-me/add-avatar/<str:username>/", add_avatar, name="add-avatar"),
    path("all-users-list/", AllUsersListView.as_view(), name="all-users-list"),
    path("register/", RegisterView.as_view(), name="register"),
    path("user-details/<int:pk>/", UserDetailsView.as_view(), name="user-details"),
    path("user-details/update-avatar/<str:username>/", update_avatar, name="update-avatar"),

    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),

    path("session/set/", set_session_view, name="session-set"),
    path("session/get/", get_session_view, name="session-get"),

    path("foo-bar/", FooBarView.as_view(), name="foo-bar"),
]