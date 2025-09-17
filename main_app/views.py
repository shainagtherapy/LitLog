from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Log, Profile

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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

@login_required
def profile(request):
    return render(request, 'users/profile.html')

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['location', 'birthday', 'favorites']
#         widgets = { 'birthday: forms.DateInput(attrs={'type': 'date }) }