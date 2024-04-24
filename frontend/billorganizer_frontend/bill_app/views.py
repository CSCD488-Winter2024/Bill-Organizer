from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def index(request):
    return HttpResponse('Hello, World!')

from .models import bill
def allbills(request):

    http = ""
    for b in bill.objects.all():
        http += "bill:{billname} \n".format(billname = b.billname)

    return HttpResponse(http)