from django.shortcuts import render
from .forms import ImageForm
from django.http import JsonResponse

from .models import Image

def main_view(request):
    # obj = Image.objects.get(pk=1)
    form = ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'works'})
    context = {'form': form}
    return render(request, 'image/index.html', context)
