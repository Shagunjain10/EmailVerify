from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from ..models import Profile

# User = get_user_model()

# class CustomTokenCreateSerializer(TokenCreateSerializer):

#     def validate(self, attrs):
#         password = attrs.get("password")
#         params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
#         self.user = authenticate(
#             request=self.context.get("request"), **params, password=password
#         )
#         if not self.user:
#             self.user = User.objects.filter(**params).first()
#             if self.user and not self.user.check_password(password):
#                 self.fail("invalid_credentials")
#         # We changed only below line
#         if self.user: # and self.user.is_active: 
#             return attrs
#         self.fail("invalid_credentials")

class AccountSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password','email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(username=validated_data['username'],email=validated_data['email'],is_active=False)
        user.set_password(password)
        user.save()
        # User.objects.create(user=user, **profile_data)
        return user
