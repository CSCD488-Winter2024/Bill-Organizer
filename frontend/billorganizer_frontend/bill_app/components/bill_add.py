from typing import List
from django_unicorn.components import UnicornView
from ..models import Bills
from django.contrib.auth import get_user
from django.http import HttpResponse
from django.template import Template
from django.template import Context
from .. import utils
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

class BillAddView(UnicornView):#TODO follow this https://docs.djangoproject.com/en/5.0/topics/class-based-views/

  def mount(self, component_args: List | None = None, **kwargs):
    self.already_clicked = False
    # Use the cursor to grab bills in sequence
    with Cursor() as cur:
      query = self.request.GET.get("q")
      if query == None:
        query = '%%'
      """
      WHERE column1 LIKE '%word1%'
      OR column2 LIKE '%word1%'
      OR column3 LIKE '%word1%'
      """
      #TODO make this not a security vulnerability
      # sql = "SELECT * FROM billorg.bills WHERE " + " LIKE '%{}%' OR ".format(query).join([ f.name for f in Bills._meta.fields + Bills._meta.many_to_many ])
      sql = "SELECT * FROM billorg.bills"
      #make a link to get bills as excel
      # filepath = utils.export_query(sql)
      # html +="<a  href='{{% static '{}' %}}' download> Download this list as CSV </a>".format(filepath) #TODO figure out when to delete the file afterward

      
      cur.execute(sql)

      rows = cur.fetchall()
      self.rows = [list(row) for row in rows]
      self.biennium_index = 0#cur.description.index('biennium')
      self.bill_id_index = 1#cur.description.index('bill_id')
  
  # def mount(self):
  #   arg = self.component_args[0]
  #   kwarg = self.component_kwargs["name"]

  #   assert (f"{arg} {kwarg}" == "Hello World", kwarg)

  def add_bill(self,row:list):
    """
    row: a list of strings of bill attributes
    
    mark the bill so it is added to the default list of the user.
    """
    user = get_user(self.request)
    list = utils.get_default_list(user)
    list_id = list.id 
    biennium = row[self.biennium_index]
    bill_id = row[self.bill_id_index]

    utils.mark_bill(list_id=list_id, biennennium=biennium, bill_id=bill_id)