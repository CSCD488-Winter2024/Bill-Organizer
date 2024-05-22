from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Bills
from django.http import HttpResponse
from django.db.models import Q 
from django.template import loader
from django.template import Template
from django.template import Context

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

from tabulate import tabulate


# Create your views here.
def index(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())

def allbills(request):
    http = ''
    http = "{% load bootstrap5 %}{% bootstrap_css %}{% bootstrap_javascript %}"
    http += '<link href="/static/css/contents.css" rel="stylesheet" type="text/css">'
    # Use the cursor to grab bills in sequence
    cur.execute("SELECT * FROM billorg.bills")

    http = http + tabulate(cur.fetchall(), tablefmt='html',)#TODO make this show column names

    # for row in cur.fetchall():
    #     http += "billname: {billname} <br> billdescription: {billdesc}<br><br>".format(billname = row[1],billdesc = row[2])


    # for b in bill.objects.all():
    #     http += "billname: {billname} <br> billdescription: {billdesc}<br><br>".format(billname = b.billname,billdesc = b.text)
    
    #process the html
    t = Template(http)
    http = t.render(Context({}))

    return HttpResponse(http)

class SearchResultsView(ListView):
    model = Bills
    template_name = 'search_results.html'
    # queryset = bill.objects.filter(billname__icontains='2')
    q = ""
    #override the inherited method
    def get_queryset(self):
        query = self.request.GET.get("q")
        if query == None:
            query = '%%'#"select * from bill_app_bill where billname like '%%'" 
        object_list = Bills.objects.raw("select * from Bills where short_description like '%{}%'".format(query))
        return object_list
    
def bootstrap_example(request):
  template = loader.get_template('master.html')
  return HttpResponse(template.render())