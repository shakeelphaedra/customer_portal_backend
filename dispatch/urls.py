from django.urls import path
from dispatch import views

urlpatterns = [
    path('login/', views.DispatchLoginView.as_view(), name='dispatch-login'),
    path('dispatches/<str:emp_no>/', views.DispatchListView.as_view(), name='dispatch-list'),
    path('dispatch/<str:disp_no>/', views.DispatchDetailView.as_view(), name='dispatch-detail'),
    path('dispatch/<str:disp_no>/parts/', views.DispatchPartsView.as_view(), name='dispatch-parts'),
    path('dispatch/<str:disp_no>/notes/', views.DispatchAddNotesView.as_view(), name='dispatch-notes'),
    path('customer/<str:cust_no>/history/', views.DispatchHistoryView.as_view(), name='dispatch-history'),
]
