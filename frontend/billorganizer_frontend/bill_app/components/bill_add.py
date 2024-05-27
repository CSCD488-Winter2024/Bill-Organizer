from django_unicorn.components import UnicornView

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
    already_clicked = False


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
      sql = "SELECT * FROM billorg.bills WHERE " + " LIKE '%{}%' OR ".format(query).join([ f.name for f in Bills._meta.fields + Bills._meta.many_to_many ])
      
      #make a link to get bills as excel
      # filepath = utils.export_query(sql)
      # html +="<a  href='{{% static '{}' %}}' download> Download this list as CSV </a>".format(filepath) #TODO figure out when to delete the file afterward

      
      cur.execute(sql)

      rows = cur.fetchall()
      rows = [list(row) for row in rows]
    
    def mount(self):
        arg = self.component_args[0]
        kwarg = self.component_kwargs["name"]

        assert (f"{arg} {kwarg}" == "Hello World", kwarg)

    #TODO call util add bill to list function. and also integrate this view into the search bills view
    def add_bill(self,bill):
        user = get_user(self.request)
        list = utils.get_default_list(user)
        utils.mark_bill(list=list,bill=bill)