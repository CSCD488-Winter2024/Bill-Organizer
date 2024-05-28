from typing import List
from django_unicorn.components import UnicornView
from ..models import Bills
from django.contrib.auth import get_user
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
biennium_index = 0#cur.description.index('biennium')
bill_id_index = 1#cur.description.index('bill_id')

class BillAddView(UnicornView):
  
#TODO fix this so it doesnt crash when you load the page pls.

  def mount(self):
    # arg = self.component_args[0]
    # kwarg = self.component_kwargs["name"]
    """
    mount is called when the component is imported by the template?
    """
    self.rows = self.component_kwargs["rows"]

  def add_bill(self,row:list):
    """
    row: a list of strings of bill attributes
    
    mark the bill so it is added to the default list of the user.
    """
    assert False
    user = get_user(self.request)
    list = utils.get_default_list(user)
    list_id = list.id 
    biennium = row[biennium_index]
    bill_id = row[bill_id_index]

    utils.mark_bill(list_id=list_id, biennennium=biennium, bill_id=bill_id)