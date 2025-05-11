# home/views.py
from django.shortcuts import render
from django.views import View


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')



# def spectaql_documentation_view(request):
#     # مسیر 'documentation/graphql/index.html' به فایل index.html
#     # داخل پوشه templates/documentation/graphql/ اشاره دارد.
#     return render(request, 'documentation/graphql/index.html')
