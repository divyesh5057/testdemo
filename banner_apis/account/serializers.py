from rest_framework import serializers
from account.models import User,Category_db,banner_db,AdminBanners




class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['id','username','email','phone_number','is_admin' ,'password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password is not same")
        
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                raise serializers.ValidationError({"password": "You cant change password."})
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
    

class UserRSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','full_name','email','phone_number','profilei_image']
 
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','profilei_image','email','phone_number','full_name','designation','date_of_birth' ,'date_of_joining','website','gender']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    
    
class UserSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username','email','phone_number','is_admin' ]
       

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                raise serializers.ValidationError({"password": "You cant change password."})
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
    
class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ['username', 'password']


class UserlogoutSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ['username']
        
class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['password','password2']
       
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password is not same")
        
        return attrs
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category_db
        fields=['id','name']
        
class BanerSerializers(serializers.ModelSerializer):
    # banner_url= serializers.SerializerMethodField()

    class Meta:
        model=banner_db
        fields=['id','category','banner_img']
        

    
class AdminBannersSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdminBanners
        fields=['id','banner_images']