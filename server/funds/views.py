from django.shortcuts import render
from django.http import HttpResponse

from .models import Funds

# Create your views here.
def index(request):
    obj = Funds.objects.first()
    return HttpResponse("%s: %s" %(obj.name, obj.fundcode))
