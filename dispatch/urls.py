from django.urls import path
from dispatch import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url


schema_view = get_schema_view(
   openapi.Info(
      title="CLS CustomerPortal API",
      default_version='v1',
      description="Schema is intended for CLS CustomerPortal",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('login/', views.DispatchLoginView.as_view(), name='dispatch-login'),
    path('dispatches/<str:emp_no>/', views.DispatchListView.as_view(), name='dispatch-list'),
    path('dispatch/<str:disp_no>/', views.DispatchDetailView.as_view(), name='dispatch-detail'),
    path('dispatch/<str:disp_no>/update-status/', views.UpdateDispatchStatus.as_view(), name='update-dispatch-status'),
    path('dispatch/<str:disp_no>/parts/', views.DispatchPartsView.as_view(), name='dispatch-parts'),
    path('dispatch/<str:disp_no>/parts/search/<str:part_name>/', views.SearchPartsView.as_view(), name='search-parts'),
    path('dispatch/<str:disp_no>/notes-availability/', views.DispatchNotesAvailabilityView.as_view(), name='dispatch-notes'),
    path('customer/<str:cust_no>/history/', views.DispatchHistoryView.as_view(), name='dispatch-history'),
]
