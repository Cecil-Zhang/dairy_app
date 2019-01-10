from .models import Diary
from rest_framework import serializers


class DiarySerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField()
    class Meta:
        model = Diary
        fields = ('id', 'datetime', 'weather', 'content', 'year', 'month', 'day')
        read_only_fields = ('id', 'year', 'month', 'day')

    def create(self, validated_data):
        diary = Diary()
        diary.datetime = validated_data['datetime']
        diary.weather = validated_data['weather']
        diary.content = validated_data['content']
        diary.populateYMD()
        diary.save()        
        return diary

    def update(self, instance, validated_data):
        instance.datetime = validated_data.get(['datetime'], instance.datetime)
        instance.weather = validated_data.get(['weather'], instance.weather)
        instance.content = validated_data.get(['content'], instance.content)
        instance.populateYMD()
        instance.save()
        return instance
