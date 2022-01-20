from rest_framework import serializers
from .models import *


class TestLogSerializer(serializers.ModelSerializer):
    json_payload = serializers.JSONField() # change is here
    json_response = serializers.JSONField() # change is here
    test_description = serializers.JSONField() # change is here
    exception = serializers.JSONField() # change is here
    api_endpoint = serializers.URLField() # change is here

    class Meta:
        model = TestLog
        fields = (
            'api_endpoint','test_name', 'request_method',
            'result','response_time','status_code','json_validation',
            'json_payload', 'json_response', 'link_checker',
            'exception', 'test_description'
                  )