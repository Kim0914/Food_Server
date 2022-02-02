from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from allergy.models import *
from allergy.serializers import *
from users.mixins import ApiAuthMixin, PublicApiMixin

User = get_user_model()

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
        user_id = kwargs["user_id"]
        allergy = Allergy.objects.get(pk=user_id)
        serializer = AllergySerializer(allergy)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):

        if kwargs.get('user_id') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            user_id = kwargs.get('user_id')
            allergy = Allergy.objects.get(id=user_id)

            update_allergy_serializer = AllergySerializer(allergy, data=request.data)
            if update_allergy_serializer.is_valid():
                update_allergy_serializer.save()
                return Response(update_allergy_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)