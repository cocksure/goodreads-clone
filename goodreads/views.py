from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from books.models import BookReview, Book, Author, Categories


class LandingPage(View):

    def get(self, request):
        books = Book.objects.all()
        search_query = request.GET.get('q', '')
        authors = Author.objects.all()
        categories = Categories.objects.all()

        context = {
            'books': books,
            'authors': authors,
            'categories': categories,
            'search_query': search_query
        }
        return render(request, 'landing.html', context)


def home_page(request):
    book_reviews = BookReview.objects.all().order_by("-created_at")

    page_size = request.GET.get('page_size', 9)
    paginator = Paginator(book_reviews, page_size)

    page_num = request.GET.get('page', 3)
    page_obj = paginator.get_page(page_num)

    context = {
        "page_obj": page_obj
    }
    return render(request, "home.html", context)
