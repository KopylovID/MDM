from typing import Dict, List, Any

class  MACreateSchema:

    @staticmethod
    def get_schema(schema_name: str, table_name: str, fields: List[Dict[str, Any]]) -> Dict:
        result = {
            'schema_name': schema_name,
            'table_name': table_name,
            'fields': fields
        }
        return result