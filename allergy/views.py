from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.dispatch import receiver
from django.db.models.signals import post_save

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from allergy.models import *
from allergy.serializers import *
from users.mixins import ApiAuthMixin, PublicApiMixin
from users.models import User

User = get_user_model()

@receiver(post_save, sender=User)
def create_Allergy(sender, instance, created, **kwargs):
    if created:
        Allergy.objects.create(user=instance)
        # print('allergy model created success')

class allergyCreateApi(ApiAuthMixin, APIView):
    def post(self, request):
        serializer = AllergySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print(serializer.validated_data)
        serializer.save(user_id=request.user.id)

        return Response({
            "message": "Allergy created success"
        }, status=status.HTTP_201_CREATED)


class allergyDetailApi(ApiAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        """
        user에 맞는 allergy 선택
        """
        allergy = Allergy.objects.get(user_id=request.user.id)
        serializer = AllergySerializer(allergy)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        """
        user에 맞는 allergy 정보 수정
        """
        allergy = Allergy.objects.get(user_id=request.user.id)

        update_allergy_serializer = AllergySerializer(allergy, data=request.data)
        if update_allergy_serializer.is_valid():
            update_allergy_serializer.save()
            return Response({
                "message": "Allergy info modify success"
            }, status=status.HTTP_200_OK)
        else:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)