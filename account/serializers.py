from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

User = get_user_model()

class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=255)
    age = serializers.IntegerField(required=False)
    nationality = serializers.CharField(required=False, max_length=255)

    password = serializers.CharField()
    password_confirmation = serializers.CharField()


    def validate(self, attrs):
        email = attrs.get('email')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exists')

        age = attrs.get('age')
        if age and age < 0:
            raise serializers.ValidationError('age can not be negative')

        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('passwords should be similar')

        nationality = attrs.get('nationality')
        if nationality and nationality in ['KG, Kyrgyzstan', 'NO', 'Norway']:
            raise serializers.ValidationError('You are too good for this app, go and use something better')

        return attrs

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        validated_data.pop('password_confirmation')

        user = User.objects.create_user(email=email, password=password, **validated_data)
        return user


class ActivateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField(max_length=10)

    def validate(self, attrs):
        email = attrs.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('user with this email does not exist')

        user = User.objects.get(email=email)
        if user.is_active:
            raise serializers.ValidationError('user is already active')

        return attrs

    def activate(self, validated_data):
        email = validated_data.get('email')
        code = validated_data.get('activation_code')

        user = User.objects.get(email=email)

        if user.activation_code == code:
            user.is_active = True
            user.activation_code = None
            user.save()
            return user

        return False



class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('user does not exist')

        user_1 = User.objects.get(email=email)
        print(user_1)

        user = authenticate(email=email, password=password)
        print(user)

        if not user:
            raise serializers.ValidationError('user was not logged in')

        attrs.update(
            {
                'user': user
            }
        )

        return attrs



class UpdateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=False)
    age = serializers.IntegerField(required=False)
    nationality = serializers.CharField(max_length=255, required=False)

    def validate (self, attrs):
        age = attrs.get('age')

        if age and age <0:
            raise serializers.ValidationError('age can not be negative')

        return attrs

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.age = validated_data.get('age', instance.age)
        instance.nationality = validated_data.get('nationality', instance.nationality)

        instance.save()

        return instance


class ConfirmedUpdateUserEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    activation_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        new_email = attrs.get('new_email')

        if User.objects.filter(email=new_email).exists():
            raise serializers.ValidationError('user with this email already exists')

        return attrs

    def update(self, instance, validated_data):
        code = validated_data.get('activation_code')
        new_email = validated_data.get('new_email')

        old_email = instance.email

        if instance.activation_code == code:
            user = User.objects.get(email=old_email)
            user.email = new_email
            user.activation_code = None
            user.save()
            return user

        return False


class ConfirmUpdateUserPasswordSerializer(serializers.Serializer):
    activation_code = serializers.CharField(max_length=10)
    new_password = serializers.CharField(max_length=25)
    password_confirmation = serializers.CharField(max_length=25)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        password_confirmation = attrs.get('password_confirmation')

        if new_password != password_confirmation:
            raise serializers.ValidationError('passwords are not somehow similar BRATER')

        return attrs

    def update(self, instance, validated_data):
        new_password = validated_data.get('new_password')
        code = validated_data.get('activation_code')

        if instance.activation_code == code:

            instance.set_password(new_password)
            instance.activation_code = None
            instance.save()
            return instance

        return False

        instance.set_password(new_password)