from django.shortcuts import render
from .forms import CroppedImageForm
from django.http import JsonResponse
from users.models import UserProfile

def cropped_image_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    form = CroppedImageForm(request.POST or None, request.FILES or None, instance=user_profile)
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'works'})
    context = {'form': form, 'profile': user_profile}
    return render(request, 'crop/crop.html', context)
