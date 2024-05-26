from django_unicorn.components import UnicornView

from django.contrib.auth import get_user
import sys
import os

from .. import utils


class ButtonAddView(UnicornView):
    already_clicked = False
    
    #TODO call util add bill to list function. and also integrate this view into the search bills view
    def add_bill(self,bill):
        user = get_user(self.request)
        list = utils.get_default_list(user)
        utils.mark_bill(list=list,bill=bill)