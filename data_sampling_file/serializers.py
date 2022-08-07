from rest_framework import serializers
from .models import StatiskIncidents, TopDataFile


"""
Сегиализатор для работы с БД файлов,
модель StatiskIncidents
"""

class MyStatistickSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatiskIncidents
        fields = "__all__"

"""
Сериализатор для работы с БД ТОП записи,
модель TopDataFile
"""

class MyTopSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopDataFile
        fields = "__all__"