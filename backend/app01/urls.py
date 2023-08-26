from django.urls import path, include
from app01 import files
urlpatterns = [
    path('variance_analysis', files.analyze_selected_columns)
]