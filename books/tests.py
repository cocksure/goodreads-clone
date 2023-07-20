from django.test import TestCase
from django.urls import reverse

from books.models import Book, Categories
from users.models import CustomUser


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found.")

    def test_books_list(self):
        category = Categories.objects.create(name='comedy')
        book1 = Book.objects.create(title="Book1", category=category, description="description1", isbn="123456789")
        book2 = Book.objects.create(title="Book2", category=category, description="description2", isbn="12345678910")
        book3 = Book.objects.create(title="Book3", category=category, description="description3", isbn="12345678911")

        response = self.client.get(reverse("books:list") + "?page_size=3")

        for book in [book1, book2, book3]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?page=2&page_size=2")

        self.assertContains(response, book3.title)

    def test_detail_page(self):
        category = Categories.objects.create(name='comedy')
        book = Book.objects.create(title="Book1", category=category, description="description1", isbn="123456789")

        response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_books(self):
        category = Categories.objects.create(name='comedy')
        book1 = Book.objects.create(title="Sport", category=category, description="description1", isbn="123456789")
        book2 = Book.objects.create(title="Great", category=category, description="description2", isbn="12345678910")
        book3 = Book.objects.create(title="Comedy", category=category, description="description3", isbn="12345678911")

        response = self.client.get(reverse("books:list") + "?q=Sport")
        self.assertContains(response, book1.title)
        self.assertContains(response, book2.title)
        self.assertContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Great")
        self.assertContains(response, book2.title)
        self.assertContains(response, book1.title)
        self.assertContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Comedy")
        self.assertContains(response, book3.title)
        self.assertContains(response, book2.title)
        self.assertContains(response, book1.title)




# class BookReviewTestCase(TestCase):
#     def test_add_review(self):
#         book = Book.objects.create(title="Book1", description="description1", isbn="123456789")
#         user = CustomUser.objects.create(
#             username="jama", first_name="Jamshid", last_name="Anorbekov", email="jama@mail.com"
#         )
#         user.set_password("somepass")
#         user.save()
#         self.client.login(username="jama", password="somepass")
#
#         self.client.post(reverse("books:reviews", kwargs={"id": book.id}), data={
#             "starts_given": 3,
#             "comment": "Nice Book"
#         })
#         book_reviews = book.bookreview_set.all()
#
#         self.assertEqual(book_reviews.count(), 1)
#         self.assertEqual(book_reviews[0].stars_given, 3)
#         self.assertEqual(book_reviews[0].comment, "Nice Book")
#         self.assertEqual(book_reviews[0].book, book)
#         self.assertEqual(book_reviews[0].user, user)


