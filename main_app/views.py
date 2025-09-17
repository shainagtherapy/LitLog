from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .models import Log, Profile
from .forms import ProfileForm

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

# Create your views here.
class Home(LoginView):
    template_name = 'home.html'

@login_required
def log_index(request):
    logs = Log.objects.filter(user=request.user)
    return render(request, 'logs/index.html', {'logs': logs})

@login_required
def log_detail(request, log_id):
    log = Log.objects.get(id=log_id) #safety alternate:    log = get_object_or_404(Log, id=log_id, user=request.user)
    return render(request, 'logs/detail.html', {'log': log})

#----- PROFILE VIEWS -----
@login_required
def profile_detail(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, "profiles/profile_detail.html", { "profile": profile })

def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile-detail')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/profile_form.html', {'form': form})
    


class LogCreate(LoginRequiredMixin, CreateView):
    model = Log
    fields = ['title', 'author', 'type', 'status', 'notes']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class LogUpdate(LoginRequiredMixin, UpdateView):
    model = Log
    fields = ['status', 'notes']

    def get_queryset(self): #only allow editing on own logs
        return Log.objects.filter(user=self.request.user)

class LogDelete(LoginRequiredMixin, DeleteView):
    model = Log
    success_url = '/logs/'

    def get_queryset(self): #only allow on own logs
        return Log.objects.filter(user=self.request.user)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('log-index')
        else:
            error_message = 'Invalid sign up - try again'
    
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

