from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_GET
from .models import Book, Author, Logging
from .forms import BookForm

# Create your views here.

def book_list(request):
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

def view_10_request():
    pass


# @require_GET
# def show_book(request, pk):
#     book = Book.objects.get(id=pk)
#     book_form = BookForm(instance=book)
#     book_form.is_valid()
#     return render(request, 'bookstore/book_form.html')


def view_logs(request):
    pass

