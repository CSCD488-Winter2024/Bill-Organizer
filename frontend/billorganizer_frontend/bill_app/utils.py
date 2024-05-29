from django.shortcuts import render
from .models import Bills, Marks, Lists
from django.contrib.auth.models import User

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


def get_lists_for_user(user:User) -> list:
    with Cursor() as cur:
        sql = "SELECT * FROM billorg.lists WHERE author = '{}' ".format(user.id)
        cur.execute(sql)
        lists = cur.fetchall()
        return lists


def mark_bill(list,bill):
    """
    Set a bill to be marked in a list (add it to the marks table.)


    -- add bills to a list
      INSERT INTO marks VALUES abcd-1234-efgh-5678 2023-24 SB-1234
       marked_bill = Marks.objects.create(list=list,biennium=bill.biennium,bill=bill)
    """
    mark = Marks.objects.create(list=list,biennium=bill.biennium,bill=bill)
    return mark
    
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