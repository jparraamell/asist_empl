from django.shortcuts import render


# Create your views here.

def input_page(request):
    return render(request, 'input.html')

def output_page(request):
    return render(request, 'output.html')  