from django.urls import path, include
from . import views 

urlpatterns = [
     path('details/<int:id>', views.DetailBookView.as_view(), name='detail_book'),
    
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
path('return_book/<int:transaction_id>/', views.return_book, name='return_book'),

]