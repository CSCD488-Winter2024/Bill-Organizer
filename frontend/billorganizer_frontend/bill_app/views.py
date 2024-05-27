from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from .models import Bills, Marks, Lists
from . import utils
from django.http import HttpResponse
from django.db.models import Q 
from django.template import loader
from django.template import Template
from django.template import Context
from django.contrib.auth import get_user
# from django_unicorn.

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
from cfg import Cursor
import util as backend_utils
from tabulate import tabulate


# Create your views here.
def index(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())

def allbills(request):
    http = ''
    http = "{% load bootstrap5 %}{% bootstrap_css %}{% bootstrap_javascript %}"
    http += '<link href="/static/css/contents.css" rel="stylesheet" type="text/css">'
    http += '{% load static %}'
    # Use the cursor to grab bills in sequence
    with Cursor() as cur:
      #make a link to get list bills as excel
      filepath = utils.export_list(None)
      http +="<a  href='{{% static '{}' %}}' download> Download this list as CSV </a>".format(filepath) #TODO figure out when to delete the file afterward

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

def SearchResultsView(request):
    http = '{% load unicorn %}{% csrf_token %}'
    http += "{% load bootstrap5 %}{% bootstrap_css %}{% bootstrap_javascript %}"
    # http = '{% extends "master.html" %}'
    http += '<link href="/static/css/contents.css" rel="stylesheet" type="text/css">'
    # Use the cursor to grab bills in sequence
    with Cursor() as cur:
      query = request.GET.get("q")
      if query == None:
        query = '%%'
      """
      WHERE column1 LIKE '%word1%'
      OR column2 LIKE '%word1%'
      OR column3 LIKE '%word1%'
      """
      #TODO make this not a security vulnerability
      sql = "SELECT * FROM billorg.bills WHERE " + " LIKE '%{}%' OR ".format(query).join([ f.name for f in Bills._meta.fields + Bills._meta.many_to_many ])
      
      #make a link to get bills as excel
      # filepath = utils.export_query(sql)
      # http +="<a  href='{{% static '{}' %}}' download> Download this list as CSV </a>".format(filepath) #TODO figure out when to delete the file afterward

      
      cur.execute(sql)

      rows = cur.fetchall()
      rows = [list(row) for row in rows]
      #add a button to the left on each row.
      button_text = "{{% unicorn 'bill-add' bill={} %}}"
      for row in rows:
        cur_button = button_text.format(row[1]) #pass bill id (2nd item in the row)

        row.insert(0, cur_button) #on the left

      http = http + tabulate(rows, tablefmt='html',)#TODO make this show column names
    
    #process the html
    t = Template(http)
    http = t.render(Context({}))

    return HttpResponse(http)

# class SearchResultsView(ListView):
#     model = Bills
#     template_name = 'search_results.html'
#     # queryset = bill.objects.filter(billname__icontains='2')
#     q = ""
#     #override the inherited method
#     def get_queryset(self):
#         query = self.request.GET.get("q")
#         if query == None:
#             query = '%%'#"select * from bill_app_bill where billname like '%%'" 
#         object_list = Bills.objects.raw("select * from billorg.bills where short_description like '%{}%'".format(query))
#         return object_list
    
def bootstrap_example(request):
  template = loader.get_template('master.html')
  return HttpResponse(template.render())



def mybills(request):
  http = ''
  http = "{% load bootstrap5 %}{% bootstrap_css %}{% bootstrap_javascript %}"
  http += '<link href="/static/css/contents.css" rel="stylesheet" type="text/css">'
  http += '{% load static %}'
  # Use the cursor to grab bills in sequence
  with Cursor() as cur: #TODO set dictionary to true
    query = request.GET.get("q")
    if query == None:
      query = '%%'
    """
    select biennium and billid from marks where uuid == <my uuid>


    -- create a list
    INSERT INTO lists (author, name) VALUES (12345, foobar) RETURNING uuid;

      list = List.objects.create(author=user,name="default")

    -- add bills to a list
    INSERT INTO marks VALUES abcd-1234-efgh-5678 2023-24 SB-1234
      marked_bill = Marks.objects.create(list=list,biennium=bill.biennium,bill=bill)

    -- get all bills in a list
    SELECT biennium, bill_id FROM marks WHERE uuid = abcd-1234-efgh-5678
    """
    if not request.user.is_authenticated:
      #user is not logged in
      return redirect('/accounts/login/')
    #user = request.user #pulled from https://stackoverflow.com/questions/12615154/how-to-get-the-currently-logged-in-users-id-in-django 
    user = get_user(request)
    #if theres no default list then make one
    list_id  = None
    if not utils.get_lists_for_user(user):
      list_id = 1
      list_id = utils.Create_list(user=user)
      list_id = 2

    mylists = utils.get_lists_for_user(user)
    #arbitrarily picking the first one for now #TODO change this to grab "default" or another requested list name
    list = mylists[0]
    #grab id (by index not key unfortunately)
    list_id = list[0] 



    #make a link to get list bills as excel
    filepath = utils.export_list(list_id)
    http +="<a  href='{{% static '{}' %}}' download> Download this list as CSV </a>".format(filepath) #TODO figure out when to delete the file afterward


    sql = "SELECT * FROM billorg.marks WHERE list = '{}' ".format(list_id)
    cur.execute(sql)

    http = http + tabulate(cur.fetchall(), tablefmt='html',)#TODO make this show column names
  
  #process the html
  t = Template(http)
  http = t.render(Context({}))

  return HttpResponse(http)