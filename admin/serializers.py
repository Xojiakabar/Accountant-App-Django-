from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from profiles.models import Job, Accountant, Comment

User = get_user_model()


class ConfirmSignUpSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_active']
        read_only_fields = ('username', 'first_name', 'last_name',)

    def update(self, instance, validated_data):
        user_id = validated_data['id']
        is_active = validated_data['is_active']
        user = User.objects.get(id=user_id)
        if is_active:
            user.is_active = True
            user.save()
            #           TODO userni emailiga siz qabul qilindingiz degan sms borishi kerak.
            return user
        else:
            user.is_active = False
            user.save()
            #             TODO userni emailiga siz qabul qilindingiz degan sms borishi kerak.
            return user


class RetrieveSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_active']
        read_only_fields = ("id" 'username', 'first_name', 'last_name', 'is_active')


# class RetrieveSignUpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'is_active']


class ListAllOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'deadline', 'client']
        read_only_fields = ('id', 'title', 'description', 'deadline', 'client')


class AttachAccountantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    # accountant = serializers.SerializerMethodField(method_name='get_accountant')
    #
    # def get_accountant(self, obj):
    #     # Get the accountant with the fewest jobs
    #     accountant_with_fewest_jobs = Accountant.objects.annotate(
    #         job_count=Count('job')
    #     ).order_by('job_count').first()
    #
    #     if accountant_with_fewest_jobs:
    #         return accountant_with_fewest_jobs.id
    #     else:
    #         return None

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'deadline', 'client', 'accountant']
        read_only_fields = ('title', 'description', 'deadline', 'client')

    def update(self, instance, validated_data):
        print(validated_data)
        job_id = validated_data['id']
        accountant = validated_data['accountant']

        accountant = get_object_or_404(Accountant, pk=accountant.id)
        job = get_object_or_404(Job, id=job_id)
        job.accountant = accountant

        job.save()
        return job


'''             Comment for client after accepting job     '''


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['description']
        read_only_fields = ['description']


''''                Director Serializer             '''


class AllJobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'deadline', 'accountant', 'client', 'status'
        ]
        read_only_fields = ('id', 'title', 'description', 'deadline', 'accountant', 'client', 'status')


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]
        read_only_fields = ('username', 'first_name', 'last_name', 'email',)


class SimpleAccountantSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Accountant
        fields = ['user', 'certificate']


class ExpiredSerialization(serializers.ModelSerializer):
    accountant = SimpleAccountantSerializer()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'deadline', 'accountant', 'client', 'status'
        ]
        read_only_fields = ('id', 'title', 'description', 'deadline', 'accountant', 'client', 'status')
