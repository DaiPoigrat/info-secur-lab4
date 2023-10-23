from django.shortcuts import render
from django.http.response import HttpResponse


# Create your views here.

def registrate(request):
    reg_data = request.POST.dict()

    usr = reg_data.get('usr', None)
    pwd = reg_data.get('pwd', None)

    print(f'{usr = }')
    print(f'{pwd = }')

    if all((usr, pwd)):


    return HttpResponse(status=201)
