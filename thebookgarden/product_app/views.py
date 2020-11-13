from django.shortcuts import render
from django.views.generic import ListView
from . import models

# Create your views here.

class BookListView(ListView):
    template_name='shop.html'
    model=models.Book
    context_name_data='booklist'   
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = models.BookCategory.objects.all()
        
        if 'pk' in self.kwargs:
            try:
                context['category_pk'] = context["categories"].filter(pk=self.kwargs.get('pk')).values('pk')[0]['pk']
            except:
                context['category_pk']=0
        else:
            try:    
                context['category_pk'] = context["categories"].first().pk    
            except:
                context['category_pk']=0

        context['booklist']=models.Book.objects.filter(book_category__id=context['category_pk'])
        context['authors']=models.Author.objects.filter(book__book_category__id=context['category_pk']).distinct()  
        query_set=context['booklist'].order_by('book_price').values('book_price')
        try:
            context['min_price']=query_set.first()['book_price']
            context['max_price']=query_set.last()['book_price']
        except:
            context['min_price']=0
            context['max_price']=0
        return context



    