from django.db import models
from rest_framework import serializers
from django.contrib.postgres.fields import ArrayField


class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()


class Image(models.Model):
    location = models.CharField(max_length=200)
    imgID = models.CharField(max_length=100, unique=True)
    annotations = ArrayField(models.TextField(blank=True), default=list)


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('url', 'subject', 'body', 'pk')


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('imgID', 'location', 'annotations', 'pk')
