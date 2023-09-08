import time

from django.utils.timezone import now
from rest_framework.generics import *
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.viewsets import *

from .permisssions import IsDirectorUser
from .serializers import *

# Create your views here.


# TODO  Ro'yhatdan o'tish uchun kelib tushgan arizalar (client or accountant)
# TODO  Buyurtmalarni bugalterlarga biriktirish
# TODO  Bugalterlarni neactive qilish
# TODO Clientlarni neactive qilish


'''
    Ro'yhatdan o'tish uchun kelib tushgan arizalar. Bugalterlar va Clientlar
'''
User = get_user_model()


class ConfirmSignUpViewSet(ModelViewSet):
    # serializer_class = ConfirmSignUpSerializer
    queryset = User.objects.filter(is_active=False).all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        method = self.request.method

        if method == 'GET':
            return RetrieveSignUpSerializer
        elif method == 'PUT':
            return ConfirmSignUpSerializer
        return ConfirmSignUpSerializer

    # def get(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)


class ListAllAccountants(ListAPIView, GenericAPIView):
    queryset = User.objects.filter(role=2).all()
    serializer_class = ConfirmSignUpSerializer
    permission_classes = [IsAdminUser]

    # def list(self, request, *args, **kwargs):
    #     return super().list(request,*args,**kwargs)


class DetailAllAccountants(RetrieveUpdateAPIView, GenericAPIView):
    queryset = User.objects.filter(role=2).all()
    serializer_class = ConfirmSignUpSerializer
    permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ListAllClients(ListAPIView, GenericAPIView):
    queryset = User.objects.filter(role=1).all()
    serializer_class = ConfirmSignUpSerializer
    permission_classes = [IsAdminUser]


class DetailAllClients(RetrieveUpdateAPIView, GenericAPIView):
    queryset = User.objects.filter(role=1).all()
    serializer_class = ConfirmSignUpSerializer
    permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ListAllOrders(ListAPIView, GenericAPIView):
    queryset = Job.objects.filter(accountant=None).all()
    serializer_class = ListAllOrdersSerializer
    permission_classes = [IsAdminUser]


class AttachAccountant(RetrieveUpdateAPIView, GenericAPIView):
    queryset = Job.objects.filter(accountant=None).all()
    serializer_class = AttachAccountantSerializer
    permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


'''                                     Director API                    '''


class AllJobs(ListAPIView, GenericAPIView):
    queryset = Job.objects.all()
    serializer_class = AllJobsSerializer
    permission_classes = [IsDirectorUser]


class DetailJobs(RetrieveAPIView, GenericAPIView):
    permission_classes = [IsDirectorUser]

    queryset = Job.objects.all()
    serializer_class = AllJobsSerializer


class AllOnProcessJobs(ListAPIView, GenericAPIView):
    queryset = Job.objects.filter(status='OP')
    serializer_class = AllJobsSerializer
    permission_classes = [IsDirectorUser]


class DetailOnProcesJobs(RetrieveAPIView, GenericAPIView):
    queryset = Job.objects.filter(status='OP')
    serializer_class = AllJobsSerializer
    permission_classes = [IsDirectorUser]


class ListDoneJobs(ListAPIView, GenericAPIView):
    queryset = Job.objects.filter(accepted_by_client=True, status='FN').all()
    serializer_class = AllJobsSerializer
    permission_classes = [IsDirectorUser]


class DetailDoneJobs(RetrieveAPIView, GenericAPIView):
    queryset = Job.objects.filter(accepted_by_client=True, status='FN').all()
    serializer_class = AllJobsSerializer
    permission_classes = [IsDirectorUser]


class ListExpiredJobs(ListAPIView, GenericAPIView):
    serializer_class = AllJobsSerializer
    queryset = Job.objects.filter(deadline__lte=now())
    permission_classes = [IsDirectorUser]

    def get_queryset(self):
        return Job.objects.filter(deadline__lt=now())


class DetailExpiredJobs(RetrieveAPIView, GenericAPIView):
    serializer_class = ExpiredSerialization
    queryset = Job.objects.filter(deadline__lte=now())
    permission_classes = [IsDirectorUser]


class DetailComment(ListAPIView, GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsDirectorUser]

    def get_queryset(self):
        job_id = self.kwargs.get('pk')
        try:
            job = Job.objects.get(id=job_id, accepted_by_client=True, status='FN')
        except:
            raise Job.DoesNotExist("The job's comments you are looking for may not exist or job may not finished yet")

        return Comment.objects.filter(job=job)
