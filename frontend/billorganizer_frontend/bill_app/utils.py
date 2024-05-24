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


def get_lists_for_user(user:User) -> list:
    with Cursor() as cur:
        sql = "SELECT * FROM billorg.lists WHERE author = '{}' ".format(user)
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