from django.shortcuts import render
from django.http import JsonResponse
from .dotify import dotify, joinDots
from io import StringIO
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .forms import GenerateForm

def index(request):
    form = GenerateForm()
    return render(request, 'dotify/index.html', {'form': form })

@csrf_exempt
def generate(request):
    if request.method == 'POST':
        form = GenerateForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.POST)
            #imageFile = request.FILES['file']
            outH = form.cleaned_data['outH']
            outW = form.cleaned_data['outW']
            thresh = form.cleaned_data['thresh']
            imageFile = form.cleaned_data['imageFile']
            reverse = form.cleaned_data['reverse']
            dots = joinDots(dotify(imageFile, thresh, outH, outW, reverse))
        else:
            dots = ''

        return JsonResponse({'dots': dots})
    else:
        return render(request, 'index.html', {'form': form})
