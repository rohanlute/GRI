from django.shortcuts import render

def brsr_list(request):
    return render(request, 'brsr/brsr_list.html')