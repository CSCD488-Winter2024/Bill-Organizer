from django_unicorn.components import UnicornView

from django.contrib.auth import get_user

from .. import utils


class BillAddView(UnicornView):
    already_clicked = False
    
    def mount(self):
        arg = self.component_args[0]
        kwarg = self.component_kwargs["name"]

        assert (f"{arg} {kwarg}" == "Hello World", kwarg)

    #TODO call util add bill to list function. and also integrate this view into the search bills view
    def add_bill(self,bill):
        user = get_user(self.request)
        list = utils.get_default_list(user)
        utils.mark_bill(list=list,bill=bill)