from django.urls import path, include
from allergy.views import *

urlpatterns = [
    # api/allergy
    path('', allergyCreateApi.as_view(), name="allergy_create"),
    path('<int:user_id>', allergyDetailApi.as_view(), name='allergyDetail'),    # 해당 유저의 알러지 정보 보여주는 URL
]
