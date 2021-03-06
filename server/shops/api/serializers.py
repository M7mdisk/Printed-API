from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from shops.models import Profile, Order,  Shop
from django.contrib.auth.models import User
class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source = 'user.id',read_only=True)
    username = serializers.CharField(source = 'user.username',validators=[UnicodeUsernameValidator(),UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(source = 'user.password', write_only = True)
    email = serializers.CharField(source = 'user.email')
    first_name = serializers.CharField(source = 'user.first_name')
    last_name = serializers.CharField(source = 'user.last_name')
    photo_url = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['id','username','email','photo_url', 'first_name','last_name','password', 'is_owner']
        extra_kwargs = {
            'password': {"write_only":True}
        }

    def get_photo_url(self, profile):
        request = self.context.get('request')
        photo_url = profile.avatar.url
        return request.build_absolute_uri(photo_url)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        profile = Profile.objects.create(user = user, **validated_data)
        return profile
    # def save(self):
    #     profile  = Profile(
    #         user.username = self.validate_data['username'],
    #         user.email = self.validate_data['email'],
    #         user.password = self.validate_data['password'],
    #         is_owner = self.validate_data['is_owner']
    #     )

class  ProfileUsingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields = ['*']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['uuid', 'buyer', 'date', 'docfile',
        'quantity', 'type', 'shop', 'total','pages', 'extension']

