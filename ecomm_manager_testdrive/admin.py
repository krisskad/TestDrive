from django.contrib import admin
from .models import TestLog


@admin.register(TestLog)
class TestLogAdmin(admin.ModelAdmin):
    list_display = ('api_endpoint','test_name', 'request_method',
                    'result','response_time','status_code','json_validation',
                    'json_response', 'link_checker',
                    'exception', 'test_description',
                    'created_at', 'updated_at')
    list_filter = ( 'test_name', 'request_method',
                    'result', 'exception',
                    'created_at', 'updated_at')
    search_fields = ['api_endpoint', 'test_name','test_description']

