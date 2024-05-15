from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import bill
from django.http import HttpResponse
from django.db.models import Q 


import sys
import os
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
project_dir = os.path.dirname(os.path.dirname(os.path.dirname(current)))
 
# adding the parent directory to 
# the sys.path.
sys.path.append(project_dir)
 
# now we can import the module in the parent
# directory.
from cfg import cur, conn

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