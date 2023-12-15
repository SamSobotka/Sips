from django.contrib.auth import login as auth_login, views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from .models import Post
from django.shortcuts import render

from . import forms, models


def get_user_themes(request):
    user_items = models.Item.objects.filter(
        transaction__userid__userid=request.user.userid
    ).values_list('itemname', flat=True)
    user_themes = [item.replace('theme_', '') for item in user_items if 'theme_' in item]
    return user_themes


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user_themes = get_user_themes(request)
    else:
        user_themes = None

    template = loader.get_template('home.html')
    context = {
        'user_themes': user_themes,
        'selected_theme': request.session.get(key='selected_theme')
    }
    return HttpResponse(template.render(context, request))


@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'feed.html', {'posts': posts})





@login_required
def message(request):  # in progress - Gianna
    template = loader.get_template('message.html')
    form = forms.MessageForm(request.POST)
    context = {
        'user_themes': get_user_themes(request),
        'selected_theme': request.session.get(key='selected_theme')
    }

    if form.is_valid():
        new_message = form.cleaned_data['message']
        return HttpResponse(new_message)

    return HttpResponse(template.render(context, request))


def password_reset(request):
    template = loader.get_template('registration/password_reset.html')
    return HttpResponse(template.render({}, request))


@login_required
def post(request):  # in progress - Zach
    template = loader.get_template('post.html')
    form = forms.PostForm(request.POST)
    context = {
        'user_themes': get_user_themes(request),
        'selected_theme': request.session.get(key='selected_theme'),
        'form': form
    }

    if form.is_valid():
        form.save()
        return redirect('/feed/')

    return HttpResponse(template.render(context, request))


@login_required
def profile(request):  # in progress - Gianna
    template = loader.get_template('profile.html')
    context = {
        'user_themes': get_user_themes(request),
        'selected_theme': request.session.get(key='selected_theme')
    }

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if not first_name or not last_name:
            return HttpResponse("Please enter valid first and last names.")

        username = first_name[0].lower() + last_name[0].lower()

        return HttpResponse("Your username is: " + username)

    return HttpResponse(template.render(context, request))


class LoginView(views.LoginView):
    form_class = forms.LoginForm
    template_name = 'registration/login.html'


def register(request):  # in-progress 💀 - Me - fixed!
    template = loader.get_template('registration/register.html')
    context = {}
    form = forms.RegisterForm(request.POST)
    context['form'] = form

    if form.is_valid():
        new_user = form.save(commit=False)

        new_user.bio = 'Hello! I\'m a new Sips user!'
        new_user.points = 0
        new_user.save()

        auth_login(request, new_user)
        return redirect('/home/')

    return HttpResponse(template.render(context, request))


def about(request):
    template = loader.get_template('about.html')
    context = {
        'user_themes': get_user_themes(request),
        'selected_theme': request.session.get(key='selected_theme')
    }
    return HttpResponse(template.render(context, request))


@login_required
def marketplace(request):  # in progress - Me
    template = loader.get_template('marketplace.html')

    themes = [
        item
        for item in models.Item.objects.all().values()
        if 'theme_' in item['itemname']
    ]

    avatars = [
        item
        for item in models.Item.objects.all().values()
        if 'avatar_' in item['itemname']
    ]

    context = {
        'user_themes': get_user_themes(request),
        'selected_theme': request.session.get(key='selected_theme'),
        'themes': themes,
        'avatars': avatars
    }

    return HttpResponse(template.render(context, request))


@login_required
def themeselection(request):  # in progress - Me - done 💀
    template = loader.get_template('themeselection.html')
    user_themes = get_user_themes(request)

    user_item_descriptions = models.Item.objects.filter(
        transaction__userid__userid=request.user.userid
    ).values_list('itemname', 'description')

    user_theme_descriptions = [
        item_description
        for user_theme, item_description in zip(user_themes, user_item_descriptions)
        if 'theme_' + user_theme == item_description[0]
    ]

    context = {
        'user_themes': user_themes,
        'selected_theme': request.session.get(key='selected_theme'),
        'descriptions': user_theme_descriptions
    }

    for theme in user_themes:
        if request.GET.get('theme_' + theme):
            if request.session.get(key='selected_theme') != theme:
                request.session['selected_theme'] = theme
            else:
                request.session['selected_theme'] = 'none'

    return HttpResponse(template.render(context, request))
