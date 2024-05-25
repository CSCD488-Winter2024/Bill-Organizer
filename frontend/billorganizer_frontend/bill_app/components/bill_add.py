from django_unicorn.components import UnicornView

#import function from utils
from 

class ButtonAddView(UnicornView):
    already_clicked = False
    
    #TODO call util add bill to list function. and also integrate this view into the search bills view
    def add_bill(self):
        self.