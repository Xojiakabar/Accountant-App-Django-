from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.generics import *
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from .permissions import *
from .serializers import *
from .models import *

# Create your views here.

'''
                        Client register, and job order views
registration        -> /register-client            ->     RegisterClientViewSet
client/             -> client/ : all orders,    client/<int:pk> : Detail, Update, Delete -> OrderJobViewSet
'''


class RegisterClientViewSet(CreateAPIView):
    serializer_class = RegisterClientSerializer
    queryset = Client.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ClientMeViewSet(ModelViewSet):
    permission_classes = [IsClient]

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user).all()

    def get_serializer_class(self):
        method = self.request.method

        return ClientSerializer

    @action(methods=['GET', 'PUT'], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Client.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = ClientSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            # Exclude the 'username' field from the data when updating
            data = request.data.copy()
            data.pop('user', None)  # Assuming 'user' is the field containing 'username'

            serializer = ClientSerializer(customer, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


'''
    Client ish zakaz qilishi uchun.
'''


class OrderJobViewSet(ModelViewSet):

    def get_serializer_class(self):
        method = self.request.method

        if method == 'POST':
            return OrderJobSerializer
        elif method == 'GET':
            return SimpleJobSerializer
        elif method == 'PUT':
            return UpdateJobSerializer
        else:
            return SimpleJobSerializer

    def get_queryset(self):
        client = get_client_from_request(self.request)
        return Job.objects.filter(client=client).all()

    def create(self, request, *args, **kwargs):
        id = Client.objects.get(user_id=self.request.user.id)
        serializer = OrderJobSerializer(data=request.data, context={'client': id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


"""
    On Processda bo'lan bugalterning barcha ishlari ko'rinib turadi.
"""


class OnProcessViewSet(ModelViewSet):
    def get_serializer_class(self):
        method = self.request.method

        if method == "GET":
            return SimpleJobSerializer
        elif method == 'PUT':
            return UpdateJobSerializer
        return SimpleJobSerializer

    def get_queryset(self):
        client = get_client_from_request(self.request)
        return Job.objects.filter(client=client, status='OP').all()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


'''
    Clientning maqullash bo'limida bugalter tomonidan yakunlangan ishlar ko'rinib turadi
     va uni tasdiqlash yoki rad etish tugmalari bo'ladi
'''


class AcceptOrDeclineViewSet(ModelViewSet):
    permission_classes = [IsClient]

    def get_serializer_class(self):
        method = self.request.method

        if method == 'GET':
            return SimpleJobSerializer
        elif method == "POST":
            return ClientJobSerializer
        elif method == 'PUT':
            return AcceptOrDeclineSerializer
        return SimpleJobSerializer

    def get_queryset(self):
        client = get_client_from_request(self.request)
        return Job.objects.filter(client=client, finish=True).filter(status='OP').all()


'''
                                Accountant View
registration -> RegisterAccountViewSet 
'''

"                                  Sign up for Accountant   "


class RegisterAccountantViewSet(GenericAPIView):
    serializer_class = RegisterAccountantSerializer
    queryset = Accountant.objects.all()

    def post(self, request):
        serializer = RegisterAccountantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


"                                   For Accountant's profile   He can use delete, put, or get requests"


class AccountantViewSet(ModelViewSet):
    serializer_class = UpdateAccountantSerializer
    permission_classes = [IsAccountant]

    @action(methods=['DELETE', 'GET'], permission_classes=[IsAccountant], detail=False)
    def me(self, reqeust):
        user = self.request.user
        accountant = get_object_or_404(Accountant, user=user)
        if accountant.user.role == 2:
            method = reqeust.method

            if method == "PUT":
                serializer = UpdateAccountantSerializer(data=reqeust.data)
                serializer.is_valid(raise_exception=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            elif method == "GET":
                serializer = RetrieveAccountantSerializer(accountant)
                return Response(serializer.data, status=status.HTTP_200_OK)

            elif method == 'DELETE':
                user.delete()
                return Response("Your data has successfully deleted ", status=status.HTTP_204_NO_CONTENT)

            else:
                return RegisterAccountantSerializer
        return Response("Siz ro'yhatdan o'tmagansiz || Yoki client emassiz")


'''
            Bugalter ishni yakunlagandan so'ng uni mijozga ko'rsatish uchun finish buttonnini bosishi kerak.
'''


class ForFinishJobViewSet(ModelViewSet):
    permission_classes = [IsAccountant]

    def get_serializer_class(self):
        method = self.request.method

        if method == 'PUT':
            return ForDoneJobSerializer
        else:
            return AccountantJobSerializer

    def get_queryset(self):
        accountant = get_accountant_from_request(self.request)
        return Job.objects.filter(accountant=accountant, status='OP').all()


'''
    Mijoz tomonidan tasdiqlangan (yani done) bo'lgan ishlar accountantning done bo'limida ko'rinib turadi.
'''


class FinishedJobViewSet(ModelViewSet):
    serializer_class = AccountantJobSerializer

    def get_queryset(self):
        accountant = get_accountant_from_request(self.request)
        return Job.objects.filter(accountant=accountant, accepted_by_client=True).all()


'''
    Admin tomonidan biriktirilgan ishlar Accountantga ko'rinib turadi
'''


class NewTaskViewSetForAccountant(ModelViewSet):
    permission_classes = [IsAccountant]
    serializer_class = AccountantJobSerializer

    def get_queryset(self):
        accountant = get_accountant_from_request(self.request)
        return Job.objects.filter(accountant=accountant, status='NS').all()

    def get_serializer_class(self):
        method = self.request.method

        if method == 'GET':
            return AccountantJobSerializer
        elif method == 'PUT':
            return UpdateAccountantJobSerializer
        return AccountantJobSerializer


'''                             Comment                     '''


class CommentView(CreateAPIView, GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsClient]

    def get_queryset(self):
        client = get_client_from_request(self.request)
        return Job.objects.filter(client=client)

    def get_serializer_context(self):
        client = get_client_from_request(self.request)

        return {'client': client}


def get_accountant_from_request(request):
    return get_object_or_404(Accountant, user=request.user)


def get_client_from_request(request):
    return get_object_or_404(Client, user=request.user)
