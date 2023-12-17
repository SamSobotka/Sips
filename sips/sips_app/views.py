from django.contrib import messages
from django.contrib.auth import login as auth_login, views
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

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
    template = loader.get_template('feed.html')
    posts = models.Post.objects.all().order_by('-postid')

    context = {
        'user_themes': get_user_themes(request),
        'selected_theme': request.session.get(key='selected_theme'),
        'posts': posts
    }
    return HttpResponse(template.render(context, request))


@login_required
def user_post(request, postid):
    template = loader.get_template('user_post.html')
    post = models.Post.objects.get(postid=postid)

    if request.POST.get('like'):
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            post.save()
            post.userid.points -= 1
            post.userid.save()
        else:
            post.likes.add(request.user)
            post.save()
            post.userid.points += 1
            post.userid.save()

    context = {
        'user_themes': get_user_themes(request),
        'selected_theme': request.session.get(key='selected_theme'),
        'post': post,
        'likes': post.likes.all()
    }
    return HttpResponse(template.render(context, request))


@login_required
def message(request):
    template = loader.get_template('message.html')
    senders = {
        user_message.senderid
        for user_message in models.Message.objects.filter(recipientid=request.user).distinct()
    }

    most_recent_messages = [
        models.Message.objects.filter(senderid=sender, recipientid=request.user).order_by('-date_created').first().content
        for sender in senders
    ]

    dict_recent_messages = {
        sender: message_
        for (sender, message_)
        in zip(senders, most_recent_messages)
    }

    context = {
        'user_themes': get_user_themes(request),
        'selected_theme': request.session.get(key='selected_theme'),
        'senders': senders,
        'recent_messages': dict_recent_messages
    }

    return HttpResponse(template.render(context, request))


def messaging(request, userid):
    template = loader.get_template('messaging.html')
    sender = models.User.objects.get(userid=userid)
    form = forms.MessageForm(request.POST)

    all_messages = models.Message.objects.filter(
        Q(recipientid=request.user, senderid=sender) |
        Q(recipientid=sender, senderid=request.user)
    ).order_by('date_created')

    print(all_messages)

    context = {
        'user_themes': get_user_themes(request),
        'selected_theme': request.session.get(key='selected_theme'),
        'sender': sender,
        'messages': all_messages,
        'form': form
    }

    if request.method == 'POST':
        if 'content' in request.POST:
            new_message = models.Message.objects.create(
                content=request.POST.get('content'),
                senderid=request.user,
                recipientid=sender
            )
            new_message.save()

    return HttpResponse(template.render(context, request))


def password_reset(request):
    template = loader.get_template('registration/password_reset.html')
    return HttpResponse(template.render({}, request))


@login_required
def create_post(request):
    template = loader.get_template('create_post.html')

    context = {
        'user_themes': get_user_themes(request),
        'selected_theme': request.session.get(key='selected_theme'),
    }

    if request.method == 'POST':
        if 'subject' in request.POST and 'content' in request.POST:
            new_post = models.Post.objects.create(
                title=request.POST.get('subject'),
                content=request.POST.get('content'),
                userid=request.user
            )
            new_post.save()
            return redirect('/feed/')

    return HttpResponse(template.render(context, request))


@login_required
def profile(request):
    template = loader.get_template('profile.html')
    form = forms.ProfileForm(request.POST, instance=request.user)
    context = {
        'user_themes': get_user_themes(request),
        'selected_theme': request.session.get(key='selected_theme'),
        'form': form
    }

    old_bio = request.user.bio

    if request.method == 'POST':
        if form.is_valid():
            update_profile = form.save(commit=False)

            if request.POST.get('bio') == '':
                update_profile.bio = old_bio

            update_profile.save()

    return HttpResponse(template.render(context, request))


class LoginView(views.LoginView):
    form_class = forms.LoginForm
    template_name = 'registration/login.html'


def register(request):
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
def marketplace(request):
    template = loader.get_template('marketplace.html')

    user_themes = get_user_themes(request)

    themes = [
        item
        for item in models.Item.objects.all().values()
        if 'theme_' in item['itemname']
    ]

    for item in models.Item.objects.all():
        if request.GET.get(item.itemname) and 'theme_' in item.itemname:
            if request.user.points < item.cost:
                messages.error(request, 'Not enough points!')
            elif item.itemname.replace('theme_', '') in user_themes:
                messages.error(request, 'You already have this theme!')
            else:
                models.Transaction.objects.create(itemid=item, userid=request.user)
                request.user.points -= item.cost
                request.user.save()
                messages.success(request, 'Successfully purchased ' + item.description)

    avatars = [
        item
        for item in models.Item.objects.all().values()
        if 'avatar_' in item['itemname']
    ]

    for item in models.Item.objects.all():
        if request.GET.get(item.itemname) and 'avatar_' in item.itemname:
            if request.user.points < item.cost:
                messages.error(request, 'Not enough points!')
            elif item.itemname.replace('avatar_', '') in user_themes:
                messages.error(request, 'You already have this theme!')
            else:
                models.Transaction.objects.create(itemid=item, userid=request.user)
                request.user.points -= item.cost
                request.user.save()
                messages.success(request, 'Successfully purchased ' + item.description)

    context = {
        'user_themes': user_themes,
        'selected_theme': request.session.get(key='selected_theme'),
        'themes': themes,
        'avatars': avatars,
        'points': request.user.points
    }

    return HttpResponse(template.render(context, request))


@login_required
def themeselection(request):
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
