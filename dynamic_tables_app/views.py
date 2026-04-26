from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .services import DynamicTableService

def json_response(data, status=200):
    return JsonResponse(data, status=status, json_dumps_params={'ensure_ascii': False})

@require_http_methods(["GET"])
def list_tables(request):
    """Список всех динамических таблиц"""
    tables = DynamicTableService.list_tables()
    return json_response({
        'tables': tables,
        'total': len(tables)
    })


@require_http_methods(["GET"])
def get_table_info(request, table_name):
    """Информация о таблице и её схеме"""
    table = DynamicTableService.get_table(table_name)
    if not table:
        return json_response({'error': f"Таблица '{table_name}' не найдена"}, 404)

    return json_response({
        'table_name': table.table_name,
        'schema': table.schema_json,
        'created_at': table.created_at.isoformat(),
        'is_active': table.is_active
    })

@require_http_methods(["GET"])
def get_records(request, table_name):
    """Получение записей из динамической таблицы"""
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 50))

        # Парсим фильтры из query parameters (формат: filter_field_name=value)
        filters = {}
        for key, value in request.GET.items():
            if key.startswith('filter_'):
                field_name = key[7:]  # убираем 'filter_'
                filters[field_name] = value

        result = DynamicTableService.get_data(table_name, filters, page, page_size)
        return json_response(result)

    except ValueError as e:
        return json_response({'error': str(e)}, 404)
    except Exception as e:
        return json_response({'error': str(e)}, 500)


@csrf_exempt
@require_http_methods(["POST"])
def create_record(request, table_name):
    """Создание записи в динамической таблице"""
    try:
        data = json.loads(request.body)
        record = DynamicTableService.create_record(table_name, data)
        return json_response({'success': True, 'record': record}, 201)
    except json.JSONDecodeError:
        return json_response({'error': 'Ошибка в формате JSON'}, 400)
    except ValueError as e:
        return json_response({'error': str(e)}, 404)
    except Exception as e:
        return json_response({'error': str(e)}, 500)


@csrf_exempt
@require_http_methods(["PUT"])
def update_record(request, table_name, record_id):
    """Обновление записи"""
    try:
        data = json.loads(request.body)
        count = DynamicTableService.update_record(table_name, record_id, data)

        if count == 0:
            return json_response({'error': f"Запись {record_id} не найдена"}, 404)

        return json_response({'success': True, 'updated': count})

    except json.JSONDecodeError:
        return json_response({'error': 'Ошибка в формате JSON'}, 400)
    except ValueError as e:
        return json_response({'error': str(e)}, 404)


@require_http_methods(["DELETE"])
def delete_record(request, table_name, record_id):
    """Удаление записи"""
    try:
        count = DynamicTableService.delete_record(table_name, record_id)

        if count == 0:
            return json_response({'error': f"Запись {record_id} не найдена"}, 404)

        return json_response({'success': True, 'deleted': count})

    except ValueError as e:
        return json_response({'error': str(e)}, 404)