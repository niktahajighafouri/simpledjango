# simpledjango / urls.py

from django.views.decorators.csrf import csrf_exempt
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from graphene_file_upload.django import FileUploadGraphQLView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home import views as home_views
urlpatterns = [
    # path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('graphql/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
    path('admin/', admin.site.urls),
    path("", include("home.urls")),
    # path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    # path("home/", include("django.contrib.auth.urls")),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path("docs/graphql/", TemplateView.as_view(template_name="graphql-docs/index.html")),
    # path("docs/graphql/", TemplateView.as_view(template_name="/public/index.html")),
    # به جاش یه ویو توی اپ home نوشتم
    # path('docs/graphql/', home_views.spectaql_documentation_view, name='spectaql_docs'),
    # path("docs/graphql/", TemplateView.as_view(template_name="docs/index.html")),
    path("docs/graphql/", TemplateView.as_view(template_name="graphqldoc/index.html")),
    # static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
