from django.shortcuts import render
from .import models
from . import forms
from django.views.generic import CreateView,UpdateView,DeleteView,DetailView
from app_users.models import UserLibraryAccount
from transaction.models import Transaction

from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.contrib import messages

from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Sum
from django.views.generic import CreateView, ListView
# Create your views here.
def send_borrowing_email(user, book, transaction, subject, template):
    message = render_to_string(template, {
        'user': user,
        'book': book,
        'transaction': transaction,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


class DetailBookView(DetailView):
    model = models.Book
    pk_url_kwarg = 'id'
    template_name = 'library_details.html'

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        book = self.get_object()

        if not self.request.user.is_authenticated:
            messages.error(request, 'You must be logged in to review books.')
            return redirect('login')

        # Check if the user has borrowed and paid for the book and hasn't returned it
        user_has_active_borrow = Transaction.objects.filter(
            account=request.user.account,
            book=book,
            paid=False  # Check if paid is True
        ).exists()

        if user_has_active_borrow:
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.book = book
                new_comment.save()
            else:
                print(comment_form.errors)
            return self.get(request, *args, **kwargs)
        else:
            messages.error(request, 'You can only review books that you have borrowed and not returned.')
            return redirect('detail_book', id=book.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        user_email = self.request.user.email if self.request.user.is_authenticated else None
        comments = book.comments.all()
        comment_form = forms.CommentForm(initial={'email': user_email})
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context


    

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(models.Book, id=book_id)
    user_account = request.user.account

    if user_account.balance >= book.borrowing_price:
        user_account.balance -= book.borrowing_price
        book.borrow_book = True
        book.save()
        user_account.save()

        borrowing_date = datetime.now()

        Transaction.objects.create(
            account=user_account,
            book=book,
            amount=book.borrowing_price,
            balance_after_transaction=user_account.balance,
            is_book_transaction=True,
            timestamp=borrowing_date,
            paid=False  # Set paid to True when borrowing
        )

        messages.success(request, f'You have successfully borrowed "{book.title}".')
        send_borrowing_email(request.user, book, borrowing_date, "Borrowed Book Message", "borrowed_book_email.html")
    else:
        messages.error(request, 'You do not have enough balance to borrow this book.')

    return redirect('detail_book', id=book_id)



@login_required
def return_book(request, transaction_id):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        transaction = get_object_or_404(Transaction, id=transaction_id)

        if not transaction.paid:
            user_account = request.user.account
            user_account.balance += transaction.amount
            user_account.save()

            transaction.paid = True  # Set paid to true when returning
            transaction.save()

            messages.success(request, 'Book returned successfully.')
        else:
            messages.error(request, 'Invalid transaction.')

    return redirect('profile')

