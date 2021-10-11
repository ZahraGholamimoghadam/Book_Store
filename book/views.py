from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from basket.models import *
from account.mixins import StaffRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import *
from django.core.paginator import Paginator

# Create your views here.


def home(request, slug=None, id=None):
    parent_categories = Category.objects.filter(is_sub_category=False)
    return render(request, 'book/home.html', {'parent_categories': parent_categories})


def most_selling_books(request, slug=None, id=None):
    most_selling_books = Book.objects.all().order_by('-number_of_sell')[:3]
    parent_categories = Category.objects.filter(is_sub_category=False)
    return render(request, 'book/most_selling_books.html', {'most_selling_books': most_selling_books,
                                                            'parent_categories': parent_categories})


def all_books(request, slug=None, id=None):
    # The following section is for displaying all books.
    books = Book.objects.all()
    paginator = Paginator(books, 7)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)  # for pagination.
    parent_categories = Category.objects.filter(is_sub_category=False)
    # The following section is for displaying books of each category.
    if slug and id:
        object = get_object_or_404(Category, slug=slug, id=id)
        books_of_category = Book.objects.filter(category=object)
        paginator = Paginator(books_of_category, 5)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
    return render(request, 'book/all_books.html', {'books': page_object, 'parent_categories': parent_categories,
                  'page_number': page_number})


def book_details(request, id):
    book = get_object_or_404(Book, id=id)
    basket_form = BasketForm()
    parent_categories = Category.objects.filter(is_sub_category=False)
    return render(request, 'book/details.html', {'book': book, 'basket_form': basket_form,
                                                 'parent_categories': parent_categories})


class SearchResultsView(ListView):
    template_name = 'book/search_results.html'
    model = Book

    def get_queryset(self):
        # In input tag in base.html we have name='input_search.'
        query = self.request.GET.get('input_search')
        return Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))


class CreateBookView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    model = Book
    form_class = CreateBookForm
    template_name = 'book/create_book.html'
    success_url = reverse_lazy('book:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_categories'] = Category.objects.filter(is_sub_category=False)
        return context


class EditBookView(StaffRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Book
    form_class = EditBookForm
    template_name = 'book/edit_book.html'
    success_url = reverse_lazy('book:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_categories'] = Category.objects.filter(is_sub_category=False)
        return context


class DeleteBookView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'book/delete_book_confirm.html'
    success_url = reverse_lazy('book:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_categories'] = Category.objects.filter(is_sub_category=False)
        return context


class CreateCategoryView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = CreateCategoryForm
    model = Category
    template_name = 'category/create_category.html'
    success_url = reverse_lazy('book:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_categories'] = Category.objects.filter(is_sub_category=False)
        return context


class CreateCashDiscountView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    model = CashDiscount
    form_class = CreateCashDiscountForm
    template_name = 'discount/create_cash_discount.html'
    success_url = reverse_lazy('book:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_categories'] = Category.objects.filter(is_sub_category=False)
        return context


class CreatePercentDiscountView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    model = PercentDiscount
    form_class = CreatePercentDiscountForm
    template_name = 'discount/create_percent_discount.html'
    success_url = reverse_lazy('book:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_categories'] = Category.objects.filter(is_sub_category=False)
        return context






