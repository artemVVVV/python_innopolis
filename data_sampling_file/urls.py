from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


#Создание роута для работы с БД через api
router = DefaultRouter()
router.register(r'api/stat', MyStatistickViewSet, basename='api/stat')
router.register(r'api/stat_all_file', MyStatistickViewSetAdmin, 
                                    basename='api/stat_all_file')
router.register(r'api/stat_top', MyTopViewSet, basename='api/stat_top')
router.register(r'api/stat_all_top', MyTopViewSetAdmin, basename='api/stat_all_top')

urlpatterns = [
    path('', LoginUser.as_view(), name='login'),
    path('my_files/', MyFileStranicty.as_view(), name = 'my_files'),
    path('all_files/', all_files, name='all_files'),
    path('add_file/', AddFile.as_view(), name='add_file'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout_user/', logout_user, name='logout_user'),
    path('', include(router.urls)), #REST api
    path('file_for_date/', FileToDate.as_view(), name='file_for_date'),
    path('work_to_text/', WorkToText.as_view(), name='work_to_text'),
]