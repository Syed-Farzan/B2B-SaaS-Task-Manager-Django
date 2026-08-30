from rest_framework import serializers

from .models import Organization, User, Membership


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization

        fields = ["id", "name", "created_at"]
        read_only_fields = ["id", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "created_at", "password"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        password = attrs.get("password")

        if len(password) < 5:
            raise serializers.ValidationError("password is too short")

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = ["organization", "user", "role"]
