from django.db import models
from rest_framework import serializers
from django.contrib.postgres.fields import ArrayField


class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()


class Image(models.Model):
    imgID = models.CharField(max_length=100, unique=True)
    extension = models.CharField(max_length=15, blank=True, default="")
    imgStaticPath = models.CharField(max_length=200)


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('url', 'subject', 'body', 'pk')


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('imgID', 'extension', 'imgStaticPath', 'pk')
