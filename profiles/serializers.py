from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from .models import *

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    role = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'role', 'is_active', 'image']
        # extra_kwargs = {'password': {'write_only': True}}


class UpdateUserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    role = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'role', 'is_active', 'image']
        extra_kwargs = {
            'password': {'write_only': True}  # Mark 'password' as write-only for security reasons
        }

    def update(self, instance, validated_data):
        # Update the writable fields of the User instance with validated_data
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.image = validated_data.get('image', instance.image)

        # If a new password is provided, securely hash and set it
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Client
        fields = ['id', 'user', 'person_type']

    def update(self, instance, validated_data):
        # Update the nested 'user' data
        user_data = validated_data.pop('user', {})
        user_serializer = UserSerializer(instance.user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()

        # Update the remaining fields of 'Client' instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the updated 'Client' instance
        instance.save()

        return instance


class RegisterClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Client
        fields = ['id', 'person_type', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=user_data['password'],
            image=user_data['image'],
            role=1,
        )

        client = Client.objects.create(user=user, **validated_data)
        return client


class OrderJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'client', 'deadline',
            'file', 'accountant', 'accepted_by_client', 'accepted_by_account'
        ]
        read_only_fields = ('id', 'client', 'accountant', 'accepted_by_client', 'accepted_by_account')

    def create(self, validated_data):
        client = self.context.get('client')
        job = Job.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            client=client,
            deadline=validated_data['deadline'],
            file=validated_data['file'],
        )
        return job


class AccountantJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id", 'title', 'description', 'deadline',
            'file', 'accountant', 'accepted_by_account', 'status'
        ]
        read_only_fields = ('status',
                            'title', 'description', 'accountant', 'file', 'deadline', 'accepted_by_account')


class UpdateAccountantJobSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Job
        fields = [
            "id", 'title', 'description', 'deadline',
            'file', 'accountant', 'accepted_by_account', 'status'
        ]
        read_only_fields = ('status',
                            'title', 'description', 'accountant', 'file', 'accepted_by_client', 'deadline',)

    def update(self, instance, validated_data):
        is_accepted = validated_data['accepted_by_account']
        job_id = validated_data['id']
        print(validated_data)
        job = Job.objects.get(id=job_id)
        if is_accepted:
            job.accepted_by_account = True
            job.status = 'OP'
            job.save()
            return job
        else:
            job.accountant = None
            job.save()
            return job


class ForDoneJobSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Job
        fields = [
            "id", 'title', 'description', 'deadline',
            'file', 'accountant', 'status', 'finish'
        ]
        read_only_fields = ('status',
                            'title', 'description', 'accountant', 'file', 'deadline',)

    def update(self, instance, validated_data):
        finish = validated_data['finish']
        job_id = validated_data['id']
        if finish:
            job = Job.objects.get(id=job_id)
            job.finish = True
            job.save()
            return job
        return validated_data


class RegisterAccountantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Accountant
        fields = ['id', 'user', 'certificate']

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=user_data['password'],
            image=user_data['image'],
            role=2,
        )

        accountant = Accountant.objects.create(user=user, **validated_data)
        return accountant


class RetrieveAccountantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Accountant
        fields = ['id', 'user', 'certificate']


class UpdateAccountantSerializer(serializers.ModelSerializer):
    user = UpdateUserSerializer()  # Assuming UpdateUserSerializer is correctly defined

    class Meta:
        model = Accountant
        fields = ['id', 'user', 'certificate']

    def update(self, instance, validated_data):
        # Update the nested 'user' data
        user_data = validated_data.pop('user', {})
        user_instance = instance.user  # Get the existing user instance
        user_serializer = UpdateUserSerializer(user_instance, data=user_data,
                                               partial=True)  # Use partial=True to allow partial updates
        if user_serializer.is_valid():
            user_serializer.save()

        # Update the remaining fields of 'Accountant' instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the updated 'Accountant' instance
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    role = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'role', 'is_active', 'image']
        extra_kwargs = {
            'password': {'write_only': True}  # Mark 'password' as write-only for security reasons
        }

    def update(self, instance, validated_data):
        # Update the writable fields of the User instance with validated_data
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.image = validated_data.get('image', instance.image)

        # If a new password is provided, securely hash and set it
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance


# class OrderJobSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     client = serializers.CharField(read_only=True)
#     accountant = serializers.CharField(read_only=True)
#     accepted_by_client = serializers.BooleanField(read_only=True)
#     accepted_by_account = serializers.BooleanField(read_only=True)
#
#     class Meta:
#         model = Job
#         fields = [
#             'id', 'title', 'description','client', 'deadline',
#             'file', 'title', 'accountant', 'accepted_by_client', 'accepted_by_account'
#         ]
#
#     def create(self, validated_data):
#         user = self.context.get('user', None)
#         print(user)
#         return f'Ok created {user}'
#
# # fields = [
# #             'id','title','description','accountant','client','deadline',
# #             'file', 'title', 'accepted_by_account','accepted_by_client'
# #         ]
#

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        read_only_fields = ('username', 'first_name', 'last_name')


class SimpleAccountantSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Accountant
        fields = ['user']


class UpdateJobSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'deadline', 'file']


class AcceptOrDeclineSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'deadline', 'file', 'accepted_by_client', 'decline']
        read_only_fields = ('title', 'description', 'deadline', 'file')

    def update(self, instance, validated_data):
        accepted_by_client = validated_data['accepted_by_client']
        decline = validated_data['decline']
        job_id = validated_data['id']

        if accepted_by_client:
            job = Job.objects.get(id=job_id)
            job.accepted_by_client = True
            job.status = 'FN'
            job.save()
            # TODO accountantni emailiga sizning ishingiz qabul qilindi degan email yuborish kerak.
            # TODO comment qismi shundan so'ng ochib briladi.
            return job
        elif decline:
            job = Job.objects.get(id=job_id)
            job.decline = True
            job.status = 'OP'
            job.save()
            # TODO accountantni emailiga sizning ishingiz qabul qilinmadi degan email yuborish kerak.
            return job
        return None


class SimpleJobSerializer(serializers.ModelSerializer):
    accountant = SimpleAccountantSerializer()

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'deadline', 'file', 'accountant', 'status']
        read_only_fields = ('id', 'title', 'description', 'deadline', 'file', 'accountant', 'status')


class ClientJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id", 'title', 'description', 'deadline',
            'file', 'accountant', 'accepted_by_client', 'status'
        ]
        read_only_fields = ('status',
                            'title', 'description', 'accountant', 'file', 'accepted_by_client', 'deadline',)


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    job = serializers.CharField()

    class Meta:
        model = Comment
        fields = ['id', 'job', 'description']

    def create(self, validated_data):
        description = validated_data['description']
        job_id = validated_data['job']
        client = self.context.get('client')

        if client is None:
            raise ValidationError('Client object is not defined. Make sure you have login...')

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            raise serializers.ValidationError("Job with the given ID does not exist.")

        if job.accepted_by_client and job.client == client:
            comment = Comment.objects.create(description=description, job=job)
            return comment

        raise serializers.ValidationError(
            "You cannot create a comment for this job. Because it belongs to another people")
