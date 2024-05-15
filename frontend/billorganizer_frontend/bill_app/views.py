from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import bill
from django.http import HttpResponse
from django.db.models import Q 
from django.template import loader


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
    q = ""
    #override the inherited method
    def get_queryset(self):
        query = self.request.GET.get("q")
        if query == None:
            query = '%%'#"select * from bill_app_bill where billname like '%%'" 
        object_list = bill.objects.raw("select * from bill_app_bill where billname like '%{}%'".format(query))
        return object_list
    
def bootstrap_example(request):
  template = loader.get_template('master.html')
  return HttpResponse(template.render())