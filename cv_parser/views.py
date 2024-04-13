# cv_parser/views.py

from django.shortcuts import render
from django.http import HttpResponse
from .cv_parser import process_cv_bundle  # Update import statement

def upload_cv(request):
    if request.method == 'POST' and request.FILES['cv_bundle']:
        cv_bundle = request.FILES['cv_bundle']
        output_file_path = process_cv_bundle(cv_bundle)
        with open(output_file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="cv_info.xlsx"'
            return response
    return render(request, 'upload_cv.html')
