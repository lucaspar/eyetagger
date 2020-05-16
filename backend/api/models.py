from django.db import models
# from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()


class Image(models.Model):
    imgID = models.CharField(max_length=100, unique=True)
    extension = models.CharField(max_length=15, blank=True, default="")
    imgStaticPath = models.CharField(max_length=200)


class Annotation(models.Model):
    annotator = models.ForeignKey('auth.User', to_field="id", related_name='annotations', on_delete=models.PROTECT)
    image = models.ForeignKey(Image, to_field="imgID", related_name='annotations', on_delete=models.PROTECT)
    annotation = models.TextField(blank=True)

    class Meta:
        unique_together = [["annotator", "image"]]


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('url', 'subject', 'body', 'pk')


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('imgID', 'extension', 'imgStaticPath', 'pk')


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ('annotator', 'image', 'annotation', 'pk')


class UserSerializer(serializers.ModelSerializer):
    annotations = serializers.PrimaryKeyRelatedField(many=True, queryset=Annotation.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'annotations']
