from rest_framework import serializers
from shops.models import Profile, Order,  Shop
from django.contrib.auth.models import User
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username',)
    password = serializers.CharField(source = 'user.password', write_only = True)
    email = serializers.CharField(source = 'user.email')
    first_name = serializers.CharField(source = 'user.first_name')
    last_name = serializers.CharField(source = 'user.last_name')
    class Meta:
        model = Profile
        fields = ['username','email', 'first_name','last_name','password', 'is_owner']
        extra_kwargs = {
            'password': {"write_only":True}
        }
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

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['uuid', 'buyer', 'date', 'docfile',
        'quantity', 'type', 'shop', 'total','pages', 'extension']