from blog.models import User
from rest_framework import serializers


class SingUpSerilizer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(write_only=True, default=False)
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "is_staff",
        )


    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)
        
