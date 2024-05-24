from django.shortcuts import render
from .models import Bills, Marks, Lists


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


def get_lists_for_user:
    sql = "SELECT * FROM billorg.marks WHERE list = '{}' ".format(list_id)
      cur.execute(sql)


def mark_bill(list,bill):
    """
    Set a bill to be marked in a list (add it to the marks table.)


    -- add bills to a list
      INSERT INTO marks VALUES abcd-1234-efgh-5678 2023-24 SB-1234
       marked_bill = Marks.objects.create(list=list,biennium=bill.biennium,bill=bill)
    """
    mark = Marks.objects.create(list=list,biennium=bill.biennium,bill=bill)
    return mark
    
def Create_list(user_id,list_name = 'default'):
    """
    -- create a list
      INSERT INTO lists (author, name) VALUES (12345, foobar) RETURNING uuid;

       list = Lists.objects.create(author=user,name="default")

    
    
    Call this function on sign *up*!
    """
    #TODO, call on user creation to make a default list

    list = Lists.objects.create(author=user_id,name=list_name)

    return list