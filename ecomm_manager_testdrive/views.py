from django.shortcuts import render
from .models import TestLog
from rest_framework import response, status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .serializers import TestLogSerializer


# Create your views here.
@csrf_exempt
@api_view(('POST',))
def store_logs(request):
    try:
        if request.method == 'POST':
            serializer = TestLogSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Unable to save data in db : ", e)
        return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"status":False, "exception":str(e)})

