from django.shortcuts import render
from django.views.generic import ListView,DetailView
from . import models
from django.http import Http404
# Create your views here.

class BookListView(ListView):
    template_name='shop.html'
    model=models.Book
    context_object_name='booklist'   
 
    def get_queryset(self):
        if 'pk' in self.kwargs:
            return self.model.objects.filter(book_category__id=self.kwargs.get('pk'))
        else:
            try:
                pk_first=models.BookCategory.objects.all().first().pk
                return self.model.objects.filter(book_category__id=pk_first)
            except:
                return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = models.BookCategory.objects.all()
        
        if 'pk' in self.kwargs:
            try:
                context['category_pk'] = context["categories"].get(pk=self.kwargs.get('pk')).pk
            except:
                raise Http404()
        else:
            try:    
                context['category_pk'] = context["categories"].first().pk    
            except:
                context['category_pk']=0

        context['authors']=models.Author.objects.filter(book__book_category__id=context['category_pk']).distinct()  
        query_set=context['booklist'].order_by('book_price').values('book_price')
        try:
            context['min_price']=query_set.first()['book_price']
            context['max_price']=query_set.last()['book_price']
        except:
            context['min_price']=0
            context['max_price']=0
        return context

class SingleBookView(DetailView):
    template_name='product-details.html'
    model=models.Book
    context_object_name='book'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_pk=self.kwargs.get('pk')
        book_images=self.model.objects.get(pk=book_pk).bookimage_set.filter(is_default=True)
        if book_images.count()>4:
            book_images=book_images[:4]
        context["book_images"] =book_images 
        return context
    


    