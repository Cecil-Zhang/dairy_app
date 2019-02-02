from .models import Diary, DiaryFile
from rest_framework import serializers
from django.contrib.auth.models import User

class DiaryFileSerializer(serializers.ModelSerializer):
    file = serializers.CharField(source="file.url")
    class Meta:
        model = DiaryFile
        fields = ('id', 'file')

class DiarySerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField()
    weather = serializers.CharField(max_length=20, required=False)
    year = serializers.IntegerField(read_only=True, required=False)
    month = serializers.IntegerField(read_only=True, required=False)
    day = serializers.IntegerField(read_only=True, required=False)
    # pictures = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='file'
    # )
    pictures = DiaryFileSerializer(many=True, read_only=True)

    class Meta:
        model = Diary
        fields = ('id', 'datetime', 'weather', 'content', 'author', 'year', 'month', 'day', 'pictures')
        read_only_fields = ('id', 'year', 'month', 'day')

    def create(self, validated_data):
        diary = Diary()
        diary.datetime = validated_data['datetime']
        diary.weather = validated_data['weather']
        diary.content = validated_data['content']
        diary.author = validated_data['author']
        diary.populateYMD()
        diary.save()        
        return diary

    def update(self, instance, validated_data):
        instance.datetime = validated_data.get('datetime', instance.datetime)
        instance.weather = validated_data.get('weather', instance.weather)
        instance.content = validated_data.get('content', instance.content)
        instance.populateYMD()
        instance.save()
        return instance
