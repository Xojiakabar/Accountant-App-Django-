from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()
router.register('confirm-sign-up', ConfirmSignUpViewSet)

# urlpatterns = router.urls

urlpatterns = [

    path('all-accountants/', ListAllAccountants.as_view()),
    path('all-accountants/<int:pk>', DetailAllAccountants.as_view()),
    path('all-clients/', ListAllClients.as_view()),
    path('all-clients/<int:pk>', DetailAllClients.as_view()),
    path('all-orders/', ListAllOrders.as_view()),
    path('all-orders/<int:pk>', AttachAccountant.as_view()),

    path('', include(router.urls)),


# '''Director urls''',

    path('all-jobs/', AllJobs.as_view()),
    path('all-jobs/<int:pk>', DetailJobs.as_view()),

    path('all-on-process-jobs/', AllOnProcessJobs.as_view()),
    path('all-on-process-jobs/<int:pk>', DetailOnProcesJobs.as_view()),

    path('all-done-jobs/', ListDoneJobs.as_view()),
    path('all-done-jobs/<int:pk>', DetailDoneJobs.as_view()),
    path('all-done-jobs/<int:pk>/comments/', DetailComment.as_view()),

    path('expired/', ListExpiredJobs.as_view()),
    path('expired/<int:pk>', DetailExpiredJobs.as_view()),
    # path('see-comment/<int:pk>', DetailComment.as_view()),
]