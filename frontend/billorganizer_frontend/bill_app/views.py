from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import bill
from django.http import HttpResponse
from django.db.models import Q 

# Create your views here.
def index(request):
    return HttpResponse('Hello, World!')

def allbills(request):

    http = ""
    for b in bill.objects.all():
        http += "billname: {billname} <br> billdescription: {billdesc}<br><br>".format(billname = b.billname,billdesc = b.text)
    return HttpResponse(http)

class SearchResultsView(ListView):
    model = bill
    template_name = 'search_results.html'
    # queryset = bill.objects.filter(billname__icontains='2')
    
    #override the inherited method
    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = bill.objects.filter(
            Q(billname__icontains=query) | Q(text__icontains=query)
        )
        return object_list