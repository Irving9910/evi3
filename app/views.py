from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, 'app/main.html')

def procesar(request):
    # val1 = request.GET["Palabra"]

    return render(request, 'app/main.html')