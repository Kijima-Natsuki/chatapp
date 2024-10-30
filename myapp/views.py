from django.shortcuts import redirect, render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse_lazy

from .models import CustomUser, TalkRoom, Message

from .forms import SignUpForm, LoginForm, MessageForm, UsernameUpdateForm, UserEmailUpdateForm, UserImageUpdateForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

from django.contrib.auth import get_user_model

User = get_user_model()

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("myapp:index")
    return render(request, "account/signup.html", {"form": form})

def login_view(request):
    form = LoginForm()
    return render(request, "account/login.html")

class FriendList(ListView):
    template_name = "myapp/friends.html"
    model = TalkRoom
    context_object_name = 'talkrooms'

    def get_queryset(self):
        query = self.request.GET.get('query')
        user = self.request.user

        talkrooms = TalkRoom.objects.filter(users=user)

        if query:
            talkrooms = talkrooms.filter(users__username__icontains=query)

        return talkrooms
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['talkrooms'] = [
            {'room': room, 'other_user': room.users.exclude(id=self.request.user.id).first()}
            for room in context['talkrooms']
        ]
        return context
    
def talk_room(request,pk):
    room = get_object_or_404(TalkRoom, id=pk)
    messages = room.messages.order_by('timestamp')
    form = MessageForm()
    other_user = room.users.exclude(id=request.user.id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.room = room
            message.sender = request.user
            message.save()
            return redirect('myapp:talk_room', pk=room.id)

    return render(request, 'myapp/talk_room.html', {'room': room, 'messages': messages, 'form': form, 'other_user': other_user})
    
def setting(request):
    return render(request, "myapp/setting.html")

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("myapp:index")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())
    
class Login(LoginView):
    template_name = 'account/login.html'
    redirect_field_name = 'redirect'
    redirect_authenticated_user = True

class Logout(LogoutView):
    pass

def get_or_create_talkroom(user1_id, user2_id):
    user1 = get_object_or_404(CustomUser, id=user1_id)
    user2 = get_object_or_404(CustomUser, id=user2_id)

    existing_rooms = TalkRoom.objects.filter(users=user1).filter(users=user2)
    if existing_rooms.exists():
        return existing_rooms.first()
    
    new_room = TalkRoom.objects.create()
    new_room.users.add(user1, user2)
    new_room.save()
    return new_room

class MyPasswordChange(PasswordChangeView):
    template_name = "myapp/password_change.html"
    success_url = reverse_lazy('myapp:password_change_done')

class MyPasswordChangeDone(PasswordChangeDoneView):
    template_name = "myapp/password_change_done.html"

def update_username(request):
    if request.method == 'POST':
        form = UsernameUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('myapp:setting')
    else:
        form = UsernameUpdateForm(instance=request.user)
    
    return render(request, 'myapp/username_change.html', {'form': form})

def update_useremail(request):
    if request.method == 'POST':
        form = UserEmailUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('myapp:setting')
    else:
        form = UserEmailUpdateForm(instance=request.user)
    
    return render(request, 'myapp/useremail_change.html', {'form': form})

def update_userimage(request):
    if request.method == 'POST':
        form = UserImageUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('myapp:setting')
    else:
        form = UserImageUpdateForm(instance=request.user)
    
    return render(request, 'myapp/userimage_change.html', {'form': form})