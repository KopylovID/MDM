from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from dynamic_tables_app.services import DynamicTableService

def json_response(data, status=200):
    return JsonResponse(data, status=status, json_dumps_params={'ensure_ascii': False})

@require_http_methods(["GET"])
def get_table_info(request, table_name):
    """Информация о таблице и её схеме"""
    table = DynamicTableService.get_table(table_name)
    if not table:
        return json_response({'error': f"Таблица '{table_name}' не найдена"}, 404)

    return json_response({
        'schema_name': table.schema_name,
        'table_name': table.table_name,
        'schema': table.schema_json,
        'created_at': table.created_at.isoformat(),
        'is_active': table.is_active
    })