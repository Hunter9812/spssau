from django.http import JsonResponse
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from chardet import detect

# file_counter = 0
@csrf_exempt
def upload(request):
    # global file_counter
    if request.method == 'POST':
        file_field = request.FILES.get('file')
        if file_field:
            file_type = os.path.splitext(file_field.name)[1].lower()
            if file_type in ['.xls', '.xlsx']:
                # 使用 pandas 读取 Excel 文件
                # file_id = str(file_counter)
                # file_counter += 1
                save_path = os.path.join(settings.MEDIA_ROOT, file_field.name)
                with open(save_path, 'wb+') as f:
                    for chunk in file_field.chunks():
                        f.write(chunk)
                df = pd.read_excel(file_field)
            elif file_type == '.csv':
                # file_id = str(file_counter)
                # file_counter += 1
                save_path = os.path.join(settings.MEDIA_ROOT, file_field.name)
                with open(save_path, 'wb+') as f:
                    for chunk in file_field.chunks():
                        f.write(chunk)
                encoding = detect(open(save_path, 'rb').read())['encoding']
                df = pd.read_csv(save_path, encoding=encoding)
            else:
                return JsonResponse({"ret": "0", "msg": "不支持该文件类型"})
             # 获取表头信息
            headers = df.columns.tolist()

            # 返回表头位置和名称
            header_info = {}
            for idx, header in enumerate(headers):
                header_info[idx] = header
            return JsonResponse({"ret": "1", "name":file_field.name, "headers": header_info})
        else:
            return JsonResponse({"ret": "0", "msg": "未收到文件"})
    else:
        return JsonResponse({"ret": "0", "msg": "仅支持 POST 请求"})
