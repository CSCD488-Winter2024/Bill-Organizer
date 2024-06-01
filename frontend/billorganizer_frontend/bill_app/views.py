from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from .models import Bills, Marks, Lists, Sponsors
from . import utils
from django.http import HttpResponse
from django.db.models import Q 
from django.template import loader
from django.template import Template
from django.template import Context
from django.contrib.auth import get_user
import json

# from django_unicorn.
from json import dumps 

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
    # Use the cursor to grab bills in sequence
    with Cursor() as cur:
      #make a link to get list bills as excel
      sql = "SELECT * FROM bills join sponsors on bills.biennium = sponsors.biennium and bills.sponsor_id = sponsors.id"
      return HttpResponse(utils.render_query(request,query=sql,query_vars = None))

def SearchResultsView(request):
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
      sql = None
      try:
        sql = backend_utils.search(query, author = get_user(request).id)
      except Exception as e:
        return HttpResponse("Error: " + str(e))
      # sql = "SELECT * FROM bills join sponsors on bills.biennium = sponsors.biennium and bills.sponsor_id = sponsors.id WHERE " + " LIKE '%?%' OR ".join([ 'bills.'+f.name for f in Bills._meta.fields + Bills._meta.many_to_many ] + [ 'sponsors.'+f.name for f in Sponsors._meta.fields + Sponsors._meta.many_to_many ])
      num_columns = len([ 'bills.'+f.name for f in Bills._meta.fields + Bills._meta.many_to_many ] + [ 'sponsors.'+f.name for f in Sponsors._meta.fields + Sponsors._meta.many_to_many ]) - 2 #subtract 2 because of joined columns
      query_array = [query]*num_columns #duplicate it for each question mark (for each column)

      

      #get bills as text and display
      return HttpResponse(utils.render_query(request,query=sql,query_vars = query_array))

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

    if not request.user.is_authenticated:
      #user is not logged in, redirect to login page
      return redirect('/accounts/login/')
    list_id = utils.get_default_list_from_request(request)

    sql = "SELECT * FROM billorg.marks \
       JOIN bills ON marks.biennium = bills.biennium AND marks.bill_id = bills.bill_id \
       JOIN sponsors ON bills.biennium = sponsors.biennium AND bills.sponsor_id = sponsors.id \
       WHERE list = '{}'".format(list_id)

    return HttpResponse(utils.render_query(request,query=sql,query_vars = None))



def bill_add(request): # see https://www.django-unicorn.com/docs/components/
  # Use the cursor to grab bills in sequence
  with Cursor() as cur:
    sql = "SELECT * FROM billorg.bills"
    
    cur.execute(sql)
    rows = cur.fetchall()
    rows = [list(row) for row in rows]
    
    js_rows = dumps(rows, default = utils.json_serial)

    context = {"rows": rows,"js_rows" :js_rows}
    return render(request, "bill_add.html", context=context)

def bill_button(request):
  row = request.GET.get("row")
  row = json.loads(row)
  print("row is:", row)

  list_id = utils.get_default_list_from_request(request)
  #TODO change these to not be hardcoded indices
  biennium = row[0]
  bill_id = row[1]
  utils.mark_bill(list_id,biennium,bill_id)

  return JsonResponse({"row is:": row})