from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Log

# Create your views here.
def home(request):
    return render(request, 'home.html')

# class Log:
#     def __init__(self, title, author, type, status, notes):
#         self.title = title
#         self.author = author
#         self.type = type
#         self.status = status
#         self.notes = notes

# logs = [
#     Log('Handmaids Tale', 'M. Atwood', 'AudioLog', 'Complete', 'Wild ride- lots of anxieety!'),
#     Log('The Sorcerers Stone', 'J.K. Rowling', 'Hardcover', 'Complete', 'Harry Potter Log 1- 5/5 reviews, reread several times!'),
#     Log('Ecstasia', 'Francesca Lia Block', 'Paperback', 'Complete', 'Fantasy Fiction retelling of the Odyssey- beautiful and feminine.')
# ]

def log_index(request):
    logs = Log.objects.all()
    return render(request, 'logs/index.html', {'logs': logs})

def log_detail(request, log_id):
    log = Log.objects.get(id=log_id)
    return render(request, 'logs/detail.html', {'log': log})

class LogCreate(CreateView):
    model = Log
    fields = '__all__'
    
class LogUpdate(UpdateView):
    model = Log
    fields = ['status', 'notes']

class LogDelete(DeleteView):
    model = Log
    success_url = '/logs/'