from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.views.decorators.http import require_GET
from .models import Book, Author, Logging, HttpRequest
from .forms import BookForm, RequestForm

# Create your views here.

def user_in_staff(user):
    return user.is_superuser or user.is_staff


def book_list(request, order=None):
    print('Order:', order)
    if order == 'desc':
        books = Book.objects.all().order_by('-publish_date')
    elif order == 'asc':
        books = Book.objects.all().order_by('publish_date')
    else:
        books = Book.objects.all()
    return render(request, 'bookstore/home.html', {'books': books})


@permission_required('bookstore.add_book')
def create_book(request):
    if request.method == 'POST':
        book_form = BookForm(request.POST, request.FILES)
        if book_form.is_valid():
            book = book_form.save()
            new_authors = book_form.cleaned_data['new_authors']
            if new_authors:
                new_authors = [item.strip() for item in new_authors.split(',')]
                for name in new_authors:
                    author = Author(fullname=name)
                    author.save()
                    book.author.add(author)
            Logging(book=book, operation='created', user=request.user.username).save()
            return redirect('book_list')
    else:
        book_form = BookForm()
    return render(request, 'bookstore/book_form.html', {'form': book_form})


@permission_required('bookstore.change_book')
def edit_book(request, pk):
    book = Book.objects.get(id=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            Logging(book=book, operation='edited', user=request.user.username).save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
        return render(request, 'bookstore/book_form.html', {'form': form})


@user_passes_test(user_in_staff)
def view_10_request(request):
    req_objects = HttpRequest.objects.all().order_by('-datetime')[:10]
    fields = [f.name for f in HttpRequest._meta.get_fields() if f.name != 'id']
    return render(request, 'bookstore/statistic.html', {'objects': req_objects, 'fields': fields, 'model': 'request'})


@user_passes_test(user_in_staff)
def view_logs(request):
    log_objects = Logging.objects.all().order_by('-date')[:10]
    fields = [f.name for f in Logging._meta.get_fields() if f.name != 'id']
    return render(request, 'bookstore/statistic.html', {'objects': log_objects, 'fields': fields, 'model': 'logging'})

