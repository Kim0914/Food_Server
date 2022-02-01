from .models import Allergy
from users.serializers import UserSerializer
from rest_framework import serializers


class AllergySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Allergy
        fields = '__all__'