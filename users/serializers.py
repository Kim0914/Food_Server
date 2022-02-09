from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        # print('create function called')
        if password is not None:
            instance.set_password(password)
        else:
            raise Exception("password is essential")

        instance.save()
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    oldpassword = serializers.CharField(write_only=True)
    newpassword = serializers.CharField(write_only=True)


    def update(self, user, validated_data):
        oldpassword = validated_data.pop('oldpassword', None)
        newpassword = validated_data.pop('newpassword', None)
        print(oldpassword)
        print(newpassword)

        if oldpassword == newpassword:
            raise serializers.ValidationError(
                "oldpassword and newpassword are same")

        print(newpassword)
        user.set_password(newpassword)
        user.save()
        return user
