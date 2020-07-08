from rest_framework.schemas.openapi import AutoSchema


class AutoSchemaWithQuery(AutoSchema):
    """
    Extending AutoSchema generation with detecting a 'query_serializer' attribute
    to generate documentation for query parameters without needing to use filters
    """
    def get_operation(self, path, method):
        operation = super(AutoSchemaWithQuery, self).get_operation(path, method)
        operation['parameters'] = self._get_query_serializer_fields()
        return operation

    def _get_query_serializer_fields(self):
        if not hasattr(self.view, 'query_serializer'):
            return []
        else:
            parameters = []
            serializer = self.view.query_serializer()
            for name, field in serializer.fields.items():
                parameters += [{
                    'name': name,
                    'in': 'query',
                    'required': field.required,
                    'description': field.help_text if field.help_text is not None else '',
                    'schema': self._map_field(field)
                }]
            return parameters
