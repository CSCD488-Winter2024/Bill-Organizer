from django.shortcuts import render, redirect
from .models import Bills, Marks, Lists
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from datetime import date, datetime
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

# def get_bill_object(biennium,bill_id) -> Bills:
#     query = "select * from bills join sponsors on bills.biennium = sponsors.biennium and bills.sponsor_id = sponsors.id where biennium = '?' and bill_id = '?'"
#     with Cursor() as cur:
#         cur.execute(query)
#         bills = cur.fetchall()
#         assert len(bills) == 1, "multiple bills with the same key and biennium were found? this shouldn't happen."
#         bill = bills[0]
#         return bill

def create_default_list(user:User) -> Lists:
    """
    create default list for user if not exist
    """
    if not get_lists_for_user(user):
      Create_list(user=user)

def get_default_list(user:User) -> Lists:
    """
    returns the default list (or just an arbitrary one. it needs to be fixed when we add more lists)
    """
    if not get_lists_for_user(user):
      create_default_list(user)

    mylists = get_lists_for_user(user)
    #arbitrarily picking the first one for now #TODO change this to grab "default" or another requested list name
    list = mylists[0]
    return list

def get_lists_for_user(user:User) -> list:
    with Cursor() as cur:
        sql = "SELECT * FROM billorg.lists WHERE author = '{}' ".format(user.id)
        cur.execute(sql)
        lists = cur.fetchall()
        return lists


def mark_bill(list_id:str,biennium:str,bill_id:str):
    """
    Set a bill to be marked in a list (add it to the marks table.)
    """
    # mark = Marks.objects.create(list=list,biennium=bill.biennium,bill=bill)
    with Cursor() as cur:
        print("list_id: ",list_id," biennium: ",biennium," bill_id: ",bill_id)
        sql = "INSERT INTO marks (list, biennium, bill_id) VALUES ('{}','{}','{}')".format(list_id,biennium,bill_id)
        mark_id = cur.execute(sql)
        return mark_id
    
def Create_list(user:User,list_name = 'default'):
    """
    -- create a list
      INSERT INTO lists (author, name) VALUES (12345, foobar) RETURNING uuid;

       list = Lists.objects.create(author=user,name="default")

    
    
    Call this function on sign *up*!
    """
    #TODO, call on user creation

    #list = Lists.objects.create(id = user.id, color = 1, author=user,name=list_name)
    with Cursor() as cur:
        sql = "INSERT INTO lists (author, name) VALUES ('{}', '{}') RETURNING id;".format(user.id,list_name)
        list_id = cur.execute(sql)
        return list_id

def export_list(list_id:str) -> str:
    """
    export the bills in a list to a query.
    """
    fullpath = backend_utils.export(list_id)
    common_path = os.path.commonpath((fullpath,current))
    relative_path = fullpath.split(common_path)[1]#format it as /static/tmp/file.csv
    #remove the extra /static since django adds one.
    relative_path = relative_path.split('/static')[1]
    return relative_path

def export_query(query:str,query_vars:list) -> str:
    """
    export the results of a query to csv 
    """
    fullpath = backend_utils.export(list_id=None,query=query,query_vars=query_vars)
    common_path = os.path.commonpath((fullpath,current))
    relative_path = fullpath.split(common_path)[1]#format it as /static/tmp/file.csv
    #remove the extra /static since django adds one.
    relative_path = relative_path.split('/static')[1]
    return relative_path

def get_default_list_from_request(request):
    if not request.user.is_authenticated:
    #   #user is not logged in
    #   return redirect('/accounts/login/')
        raise Exception("user is not logged in.")
    #user = request.user #pulled from https://stackoverflow.com/questions/12615154/how-to-get-the-currently-logged-in-users-id-in-django 
    user = get_user(request)
    #if theres no default list then make one
    list_id  = None
    if not get_lists_for_user(user):
      list_id = 1
      list_id = Create_list(user=user)
      list_id = 2

    mylists = get_lists_for_user(user)
    #arbitrarily picking the first one for now #TODO change this to grab "default" or another requested list name
    list = mylists[0]
    #grab id (by index not key unfortunately)
    list_id = list[0] 
    return list_id

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def render_query(request,query:str,query_vars:list,use_buttons=False):
    headers = []
    with Cursor(dictionary=True) as cur:
        cur.execute(query,query_vars)
        headers = cur.description
        headers = [i[0] for i in headers]

    with Cursor() as cur:
        #get bills as csv and link to file.
        filepath = export_query(query,query_vars)
        cur.execute(query,query_vars)
        rows = cur.fetchall()
        rows = [list(row) for row in rows]
        context = {"rows": rows, "link" : filepath, "headers": headers}
        js_rows = dumps(rows, default = json_serial) 
        context["js_rows"] = js_rows
        if use_buttons:
            return render(request, "bill_add.html", context=context)
        else:
            return render(request, "bills_view.html", context=context)