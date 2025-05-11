# accounts / views.py
from django.shortcuts import render, redirect
from django.views import View
from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileView(LoginRequiredMixin, View):
    # این کد به این معنی است که کاربر باید وارد حساب کاربری خود شده باشد تا دسترسی داشته باشد
    def get(self, request):
        user = request.user
        form = ProfileForm(instance=user)
        return render(request, 'profile.html', {'form': form})

    def post(self, request):
        user = request.user
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # بعد از ذخیره تغییرات، به پروفایل هدایت می‌شود
        return render(request, 'profile.html', {'form': form})

# from django.shortcuts import render, redirect
# from .forms import ProfileForm
# from django.contrib.auth.decorators import login_required


# @login_required
# def profile_view(request):
#     user = request.user
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')  # بعد از ذخیره تغییرات، به پروفایل هدایت می‌شود
#     else:
#         form = ProfileForm(instance=user)
#
#     return render(request, 'profile.html', {'form': form})
