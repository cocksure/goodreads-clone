from django.contrib import admin
from .models import Book, BookAuthor, BookReview, Author, Categories


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')
    list_display = ('id', 'title', 'category', 'isbn', 'description')
    list_filter = ('category', )


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'email')


class BookAuthorAdmin(admin.ModelAdmin):
    search_fields = ('book', 'author')
    list_display = ('id', 'book', 'author')


class BookReviewAdmin(admin.ModelAdmin):
    search_fields = ('user', 'book')
    list_display = ('id', 'user', 'book', 'stars_given')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(Categories, CategoryAdmin)
