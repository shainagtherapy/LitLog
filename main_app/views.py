# API coding:
import os, time, base64, requests

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
from django.contrib import messages


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
    log = get_object_or_404(Log, id=log_id, user=request.user)
    return render(request, 'logs/detail.html', {'log': log})

# ********** SPOTIFY API INSTRUCTIONS ********** q = query   |   r = request/req

_TOKEN_CACHE = {"access_token": None, "expires_at": 0}

def _get_spotify_token():
    # Client Credentials flow (no user scopes needed for catalog metadata).
    if _TOKEN_CACHE["access_token"] and _TOKEN_CACHE["expires_at"] > time.time() + 60:
        return _TOKEN_CACHE["access_token"]

    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in your environment.")

    token_url = "https://accounts.spotify.com/api/token"
    creds_b64 = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {"Authorization": f"Basic {creds_b64}"}
    data = {"grant_type": "client_credentials"}

    resp = requests.post(token_url, headers=headers, data=data, timeout=10)

    try:
        payload = resp.json()
    except ValueError:
        payload = {"error": f"Non-JSON token response (status {resp.status_code})"}

    if resp.status_code != 200:
        raise RuntimeError(f"Spotify token error {resp.status_code}: {payload}")

    token = payload.get("access_token")
    if not token:
        raise RuntimeError(f"Token response missing access_token: {payload}")

    _TOKEN_CACHE["access_token"] = token
    _TOKEN_CACHE["expires_at"] = time.time() + int(payload.get("expires_in", 3600))
    return token

def _spotify_search_audiobooks(q, market="US", limit=10):
    # Return list of dicts: title, author, image_url from Spotify Search (type=audiobook).
    token = _get_spotify_token()
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": q, "type": "audiobook", "market": market, "limit": limit}

    r = requests.get(url, headers=headers, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    items = (data.get("audiobooks") or {}).get("items", [])
    results = []
    for it in items:
        title = it.get("name")
        authors = ", ".join(a.get("name") for a in it.get("authors", []))
        images = it.get("images") or []
        image_url = images[0]["url"] if images else None
        results.append({"title": title, "author": authors, "image_url": image_url})
    return results


    # if q:
    #     try:
    #         token = _get_spotify_token()
    #         resp = requests.get(
    #             "https://api.spotify.com/v1/search",
    #             headers={"Authorization": f"Bearer {token}"},
    #             params={"q": q, "type": "audiobook", "market": "US", "limit": 12},
    #             timeout=10,
    #         )
    #         data = resp.json()  # Spotify always returns JSON on this endpoint

    #         if resp.status_code != 200:
    #             # Surface Spotify’s message in your template
    #             error_message = data.get("error", {}).get("message", "Unexpected error from Spotify.")
    #         else:
    #             items = (data.get("audiobooks") or {}).get("items", [])
    #             for b in items:
    #                 results.append({
    #                     "id": b.get("id"),
    #                     "title": b.get("name"),
    #                     # authors is a list of {name: "..."}
    #                     "author": ", ".join([a.get("name") for a in b.get("authors", [])]) or b.get("publisher", ""),
    #                     "image": (b.get("images") or [{}])[0].get("url"),
    #                     "external_url": (b.get("external_urls") or {}).get("spotify"),
    #                     "uri": b.get("uri"),
    #                 })
    #     except Exception as e:
    #         error_message = str(e)

    # return render(request, "audiobook-search", {
    #     "query": q,
    #     "results": results,
    #     "error_message": error_message,
    # })

# ********************* Spotify Views for Audiobook Search & Saving ********************
@login_required
def audiobook_search(request):
    q = request.GET.get("q", "").strip()
    results = _spotify_search_audiobooks(q) if q else []
    return render(request, "logs/audiobook_search.html", {"q": q, "results": results})


@login_required
def audiobook_save(request):
    if request.method != "POST":
        return redirect("audiobook-search")
    title = request.POST.get("title", "").strip()
    author = request.POST.get("author", "").strip()
    # NOTE: Your Log.cover is an ImageField; storing a remote URL there needs a download.
    # For now we’ll ignore cover, and you can add a URL field later (see note below).
    if not title:
        messages.error(request, "Missing title.")
        return redirect("audiobook-search")
    Log.objects.create(
        user=request.user,
        title=title,
        author=author,
        type="audiobook",
        status="currently reading",
        notes="Imported from Spotify search",
    )
    messages.success(request, f"Saved “{title}”.")
    return redirect("log-index")




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
            messages.success(request, "Profile updted!")
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



# API start from DEV website
# @login_required
# def get_entries(request):
#     all_entries = {}
#     if 'name' in request.GET:
#         name = request.GET['name']
#         url = 'https://api.spotify.com/v1/audiobooks/7iHfbu1YPACw6oZPAFJtqe' % nameresponse = requests.get(url)
#         data = response.json()
#         entries = data['entries']

#         for i in entries:
#             entry_data = Entry(
#                 cover = i['strCover'],
#                 title = i['strTitle'],
#                 author = i['strAuthor']
#             )
#             entry_data.save()
#             all_logs = Entry.objects.all().order_by('-id')
#     return render (request, 'logs/index.html', { "all_entries": all_entries })

