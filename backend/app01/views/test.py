import os

import pandas as pd
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def my_view(request):
    file_name = request.POST.get("name")
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    data = pd.read_excel(file_path)
    print(data)
    return JsonResponse({"data": file_path})
