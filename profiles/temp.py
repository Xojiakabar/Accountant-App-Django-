

#
#
# class OrderListApiView(ListAPIView):
#     serializer_class = SimpleJobSerializer
#
#     def get_queryset(self):
#         client = get_client_from_request(self.request)
#         return Job.objects.filter(client=client).all()
#
#
# class OrderDetailApiView(RetrieveAPIView):
#     serializer_class = SimpleJobSerializer  # update qismi qushilishi keark UpdateJobSerializer
#
#     def get_queryset(self):
#         client = get_client_from_request(self.request)
#         return Job.objects.filter(client=client).all()


# class OnProcessListView(ListAPIView):
#     serializer_class = SimpleJobSerializer
#
#     def get_queryset(self):
#         client = get_client_from_request(self.request)
#         return Job.objects.filter(client=client,status='OP').all()
#
#
# class OnProcessDetailView(ListAPIView):
#     serializer_class = SimpleJobSerializer
#
#     def get_queryset(self):
#         client = get_client_from_request(self.request)
#         return Job.objects.filter(client=client,status='OP').all()
#



# class OrderJobViewSet1(CreateAPIView):
#     queryset = Job.objects.all()
#     serializer_class = OrderJobSerializer
#     permission_classes = [IsClient]
#
#     def create(self, request, *args, **kwargs):
#         id = Client.objects.get(user_id=self.request.user.id)
#         serializer = OrderJobSerializer(data=request.data, context={'client': id})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
