from django.urls import path
from .views import (
    # Object
    MAIndexView,
    MAObjectCreateView,
    MAObjectUpdateView,
    MAObjectDeleteView,
    # Column
    MAObjectColumnListView,
    MAObjectColumnCreateView,
    MAObjectColumnUpdateView,
    MAObjectColumnDeleteView,
    # Reg Objects
    MARegObjectView,
    MAToApproveObjectView
)

app_name = "ma"

urlpatterns = [
    # Object
    path("", MAIndexView.as_view(), name="index"),
    # path('about/', about, name='about'),
    # path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path("object/add/", MAObjectCreateView.as_view(), name="object_add"),
    path("object/<int:pk>/edit/", MAObjectUpdateView.as_view(), name="object_edit"),
    path("object/<int:pk>/delete/", MAObjectDeleteView.as_view(), name="object_delete"),
    # Column
    path("object_column/<int:dictionary_id>/", MAObjectColumnListView.as_view(), name="object_column"),
    path("object_column/<int:dictionary_id>/add/", MAObjectColumnCreateView.as_view(), name="object_column_add"),
    path("object_column/<int:dictionary_id>/edit/<int:pk>/", MAObjectColumnUpdateView.as_view(), name="object_column_edit"),
    path("object_column/<int:dictionary_id>/delete/<int:pk>", MAObjectColumnDeleteView.as_view(), name="object_column_delete"),
    # Reg Objects
    path("reg_object/", MARegObjectView.as_view(), name="reg_object"),
    path("to_approve_object/", MAToApproveObjectView.as_view(), name="to_approve_object"),
]
