from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
def daskboard_principal(request):
    # Tu lógica para la vista principal de darkboard
    return render(request, 'daskboard/daskboard.html', context={})

