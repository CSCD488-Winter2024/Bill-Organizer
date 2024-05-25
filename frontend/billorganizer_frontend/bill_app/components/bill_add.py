from django_unicorn.components import UnicornView

#import function from utils
from 

class ButtonAddView(UnicornView):
    already_clicked = False

    def add_bill(self):
        self.