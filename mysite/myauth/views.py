from random import random

from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from django.views.decorators.cache import cache_page
from django.utils.translation import gettext_lazy as _, ngettext

from .forms import AboutMe, AboutMeUpdate
from .models import Profile

class HelloView(View):
    welcome_message = _("welcome hello world!")
    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get("items") or 0
        items = int(items_str)
        products_line = ngettext(
            "one product",
            "{count} products",
            items
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f"<h1>{self.welcome_message}</h1>"
            f"\n<h2>{products_line}</h2>"
        )

class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = AboutMe()
        context['form'] = form

        return context


@login_required
def add_avatar(request: HttpRequest, username):
    profile = get_object_or_404(Profile, user__username=username)

    if profile.user != request.user:
        return redirect("myauth:login")

    form = AboutMe(request.POST or None,
                   files=request.FILES or None,
                   instance=profile)

    if form.is_valid():
        form.save()

        return redirect("myauth:about-me")

    return redirect("myauth:login")



class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=password, profile=profile)
        login(request=self.request, user=user)


        return response

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/admin/')

        return render(request, 'myauth/login.html')

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin/')

    return render(request, 'myauth/login.html', {"error": "Invalid login credentials"})


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")

@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response
@cache_page(60 * 2)
def get_cookie_view(request:HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value {value!r} + {random()}")

@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")

@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")

class FooBarView(View):
    def get(self, request: HttpRequest)-> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})

class AllUsersListView(ListView):
    template_name = "myauth/all-users-list.html"
    model = Profile
    context_object_name = "profiles"
    queryset = Profile.objects.all()

class UserDetailsView(DetailView):
    template_name = "myauth/user-details.html"
    model = Profile
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = AboutMeUpdate()
        context['form'] = form

        return context

@login_required
def update_avatar(request: HttpRequest, username):
    if request.user.is_staff:
        profile = get_object_or_404(Profile, user__username=username)

        form = AboutMeUpdate(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()

            return redirect("myauth:all-users-list")