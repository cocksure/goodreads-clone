from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from books.forms import BookReviewForm
from books.models import Book, BookReview, Categories, BookAuthor, Author


# class BooksView(ListView):
#     template_name = "books/list.html"
#     queryset = Book.objects.all()
#     context_object_name = "books"
#     paginate_by = 3


class AuthorsView(View):
    def get(self, request):
        authors = Author.objects.all().order_by('-id')

        context = {
            'authors': authors
        }
        return render(request, 'authors/authors_list.html', context)


def search_books(query):
    books = Book.objects.filter(title__icontains=query)
    return books


class BooksView(View):
    def get(self, request):
        categories = Categories.objects.all()
        search_query = request.GET.get('q', '')
        books = search_books(search_query) if search_query else Book.objects.all().order_by('id')

        page_size = request.GET.get("page_size", 4)
        paginator = Paginator(books, page_size)

        page_num = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_num)

        context = {
            'categories': categories,
            'page_obj': page_obj,
            'search_query': search_query
        }

        return render(request, "books/list.html", context)


class ComedyBookView(ListView):
    template_name = 'books/comedy.html'
    context_object_name = 'comedy_books'
    paginate_by = 3

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        return search_books(search_query) if search_query else Book.objects.filter(category_id=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        return context


class FantasticBookView(ListView):
    template_name = 'books/fantastic.html'
    context_object_name = 'fantastic_books'
    paginate_by = 3

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        return search_books(search_query) if search_query else Book.objects.filter(category_id=2)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        return context


class DetectiveBookView(ListView):
    template_name = 'books/detective.html'
    context_object_name = 'detective_books'
    paginate_by = 3

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        return search_books(search_query) if search_query else Book.objects.filter(category_id=3)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        return context


# class BookDetailView(DetailView):
#     template_name = "books/detail.html"
#     pk_url_kwarg = "id"
#     model = Book


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm()
        context = {
            "book": book,
            "review_form": review_form
        }
        return render(request, "books/detail.html", context)


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm()

        if request.method == 'POST':
            review_form = BookReviewForm(request.POST)
            if review_form.is_valid():
                BookReview.objects.create(
                    book=book,
                    user=request.user,
                    stars_given=review_form.cleaned_data['stars_given'],
                    comment=review_form.cleaned_data['comment']
                )
                return redirect(reverse("books:detail", kwargs={"id": book.id}))

        return render(request, "books/detail.html", {"book": book, "review_form": review_form})


class UpdateBookReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review)
        context = {
            "book": book,
            "review": review,
            "review_form": review_form,
        }
        return render(request, "books/edit_review.html", context)

    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse("books:detail", kwargs={"id": book.id}))

        context = {
            "book": book,
            "review": review,
            "review_form": review_form,
        }
        return render(request, "books/edit_review.html", context)


class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        context = {
            'book': book,
            'review': review
        }
        return render(request, "books/confirm_delete_review.html", context)


class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)

        review.delete()
        messages.success(request, "You have successfully deleted this review")

        return redirect(reverse("books:detail", kwargs={"id": book_id}))


class AuthorsDetailView(View):
    def get(self, request, id):
        author = Author.objects.get(id=id)

        context = {
            'author': author
        }
        return render(request, 'authors/authors_detail.html', context)

