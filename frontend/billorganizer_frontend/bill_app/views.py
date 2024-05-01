from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import bill
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Hello, World!')

def allbills(request):

    http = ""
    for b in bill.objects.all():
        http += "billname: {billname} <br> billdescription: {billdesc}<br><br>".format(billname = b.billname,billdesc = b.text)
    return HttpResponse(http)


class HomePageView(TemplateView):
    template_name = 'home.html'

class SearchResultsView(ListView):
    model = bill
    template_name = 'search_results.html'