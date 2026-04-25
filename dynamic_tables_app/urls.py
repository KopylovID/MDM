from django.urls import path
from . import views

app_name = "dta"

urlpatterns = [
    path('list/', views.list_tables, name='list_tables'),
    path('<str:table_name>/', views.get_records, name='get_table_data'),
    path('<str:table_name>/ir/', views.create_record, name='insert_data'),
    path('<str:table_name>/ur/', views.update_record, name='update_data'),
    path('<str:table_name>/dr/', views.delete_record, name='delete_data'),
    # манипуляции с таблицей
    path('', views.create_table, name='create_table'),
    path('<str:table_name>/dt/', views.delete_table, name='delete_table'),
]