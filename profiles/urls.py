from django.urls import path, include
# from rest_framework import routers
from rest_framework_nested import routers
from .views import *

router = routers.DefaultRouter()

router.register('accept-or-decline', AcceptOrDeclineViewSet, 'accept-or-decline')
router.register('order-job', OrderJobViewSet, 'order-job') # All orders,detail, put, delete. ish zakaz qilish
router.register('client', ClientMeViewSet, 'client') # All orders,detail, put, delete. ish zakaz qilish

router.register('accountant', AccountantViewSet, 'accountant') # me,
router.register('on-process', OnProcessViewSet, basename='test') # On Process da bo'gan barcha ishlar list, detail,
router.register('new-tasks', NewTaskViewSetForAccountant, 'new-task') # admin tomonidan yuklangan ishlarni qabul qilish.
router.register('for-finish-job', ForFinishJobViewSet, 'for-finish-job') #  ishni tugallagandan kegin finish buttinini bosadi, list, detail finish button
router.register('finished-job', FinishedJobViewSet, 'finished-job') # status='FN' va client accept qilgan ishlar

urlpatterns = [
    path('register-client/', RegisterClientViewSet.as_view()),
    path('register-accountant/', RegisterAccountantViewSet.as_view()),
    path('comment/', CommentView.as_view()),
    path('', include(router.urls)),

]

# account/me -> profile get, delete, put.
# account/new-tasks  get. ModelMixin lar bilan harakat qilish kerak.
# account/new/<int:pk> job detail put, get.  Yuqoridagi 2 apiga router.register('new-tasks',AccountantJobView,'new-task') shu yo'l javob beradi.
# account/on-process statusi jarayonda bo'lgan ishlar kelib tushadi.
# account/done statusi done bo'lgan ishlar saqlanadi. statusi done bo'lishi uchun client accept qilishi kerak


# client/me - client profile DONE
# client/order-job To order new job DONE
# client/all-order The Jobs client has ordered DONE
# client/all-order/<int:pk> Detail DONE
# client/on-process The Jobs which is given by accountant, DONE
# clinet/maqullash uchun -> Accept or Decline buttunlari bo'ladi accept bo'lsa comment ochiladi DONE
# client/task/<int:pk>/comment Comment qoldiradi TODO comment qoldirish uchun cod yozish kerak.


# TODO Director va Admin Panellari yoziladi,