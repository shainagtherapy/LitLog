from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

class Book:
    def __init__(self, title, author, type, status, notes):
        self.title = title
        self.author = author
        self.type = type
        self.status = status
        self.notes = notes

logs = [
    Book('Handmaids Tale', 'M. Atwood', 'Audiobook', 'Complete', 'Wild ride- lots of anxieety!'),
    Book('The Sorcerers Stone', 'J.K. Rowling', 'Hardcover', 'Complete', 'Harry Potter Book 1- 5/5 reviews, reread several times!'),
    Book('Ecstasia', 'Francesca Lia Block', 'Paperback', 'Complete', 'Fantasy Fiction retelling of the Odyssey- beautiful and feminine.')
]

def log_index(request):
    return render(request, 'logs/index.html', {'logs': logs})