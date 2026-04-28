from django.urls import path
from .views import views, DTADynModelListView, DTADynModelRecordView, DynamicRecordCreateView, DynamicRecordDeleteView, DynamicRecordUpdateView

app_name = "dta"

urlpatterns = [
    path('list/', DTADynModelListView.as_view(), name='list_tables'),
    path('<str:table_name>/info/', views.get_table_info, name='get_table_info'),
    path('<str:table_name>/', DTADynModelRecordView.as_view(), name='get_table_data'),
    path('<str:table_name>/ir/', DynamicRecordCreateView.as_view(), name='insert_data'),
    path('<str:table_name>/ur/<int:record_id>', DynamicRecordUpdateView.as_view(), name='update_data'),
    path('<str:table_name>/dr/<int:record_id>', DynamicRecordDeleteView.as_view(), name='delete_data'),
]