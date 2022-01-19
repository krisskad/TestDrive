from django.db import models


# Create your models here.
class TestLog(models.Model):
    api_endpoint = models.URLField(blank=True, null=True)
    request_method = models.CharField(max_length=255, blank=True, null=True)
    test_name = models.CharField(max_length=255, blank=True, null=True)
    result = models.BooleanField(blank=True, null=True)
    status_code = models.BooleanField(blank=True, null=True)
    json_validation = models.BooleanField(blank=True, null=True)
    response_time = models.FloatField(blank=True, null=True)
    json_response = models.TextField(blank=True, null=True)
    link_checker = models.BooleanField(blank=True, null=True)
    exception = models.CharField(max_length=255, blank=True, null=True)
    test_description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.api_endpoint

