import django.views.decorators.http
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
      return HttpResponse(utils.render_query(request,query=sql,query_vars = None,use_buttons=True))

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
      query_vars = None
      try:
        sql,query_vars = backend_utils.search(query, author = get_user(request).id)
      except Exception as e:
        return HttpResponse("Error: " + str(e))

      #get bills as text and display
      return HttpResponse(utils.render_query(request,query=sql,query_vars = query_vars,use_buttons=True)) #query_array))

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

    return HttpResponse(utils.render_query(request,query=sql,query_vars = None,use_buttons=False))


def get_note(request, biennium: str, bill_id: str):
  if not request.user.is_authenticated:
    return redirect('/accounts/login/')

  with Cursor() as cur:
    cur.execute("SELECT content FROM billorg.notes where author = ? and biennium = ? and bill_id = ?", (request.user.id, biennium, bill_id))
    return HttpResponse(cur.fetchone())


def write_note(request, biennium: str, bill_id: str):
  if not request.user.is_authenticated:
    return redirect('/accounts/login/')

  with Cursor() as cur:
    cur.execute("""
      insert into notes (author, edit_time, biennium, bill_id, content)
      values (?, default, ?, ?, ?)
      on duplicate key update 
        edit_time = default,
        content = value(content)
    """, (request.user.id, biennium, bill_id, json.loads(request.body).get('text')))

  return HttpResponse()


def bill_add(request): # see https://www.django-unicorn.com/docs/components/
  # Use the cursor to grab bills in sequence
  with Cursor() as cur:
    if not request.user.is_authenticated:
      #user is not logged in, redirect to login page
      return redirect('/accounts/login/')
    sql = "SELECT * FROM billorg.bills"
    
    return HttpResponse(utils.render_query(request,query=sql,query_vars = None,use_buttons=True))
    # cur.execute(sql)
    # rows = cur.fetchall()
    # rows = [list(row) for row in rows]
    
    # js_rows = dumps(rows, default = utils.json_serial)

    # context = {"rows": rows,"js_rows" :js_rows}
    # return render(request, "bill_add.html", context=context)

def bill_button(request):
  row = request.GET.get("row")
  row = json.loads(row)
  print("row is:", row)
  # if not request.user.is_authenticated: #TODO move this to javascript to make it actually work https://stackoverflow.com/a/30145534
  #     #user is not logged in, redirect to login page
  #     return redirect('/accounts/login/')
  list_id = utils.get_default_list_from_request(request)
  #TODO change these to not be hardcoded indices
  biennium = row[0]
  bill_id = row[1]
  utils.mark_bill(list_id,biennium,bill_id)

  return JsonResponse({"row is:": row})
def add_all_button(request):
  rows = request.GET.get("rows")
  rows = json.loads(rows)
  print("rows are:", rows)
  # if not request.user.is_authenticated: #TODO move this to javascript to make it actually work https://stackoverflow.com/a/30145534
  #     #user is not logged in, redirect to login page
  #     return redirect('/accounts/login/')
  list_id = utils.get_default_list_from_request(request)
  for row in rows:
    #TODO change these to not be hardcoded indices
    biennium = row[0]
    bill_id = row[1]
    utils.mark_bill(list_id,biennium,bill_id)

  return JsonResponse({"rows are:": rows})