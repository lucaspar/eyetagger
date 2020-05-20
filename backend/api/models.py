from django.db import models
# from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()


class Image(models.Model):

    lens_types = [
        ('L', 'Live Lens'),
        ('F', 'Fake Lens'),
        ('C', 'Clear Lens'),
    ]
    eye_types = [
        ('L', 'Left Eye'),
        ('R', 'Right Eye'),
    ]
    nir_illumination = [
        ('C', 'Cross NIR'),
        ('D', 'Direct NIR'),
    ]

    img_id              = models.CharField(max_length=100, unique=True)
    extension           = models.CharField(max_length=15, blank=True, default="")
    img_path            = models.CharField(max_length=200)
    user_id             = models.CharField(max_length=100)
    sample_id           = models.IntegerField()
    eye                 = models.CharField(max_length=1, blank=True, choices=eye_types)
    lens_type           = models.CharField(max_length=1, blank=True, choices=lens_types)
    nir_illumination    = models.CharField(max_length=1, blank=True, choices=nir_illumination)
    lens_brand          = models.CharField(max_length=100, blank=True)
    is_regular          = models.BooleanField(null=True)


class Annotation(models.Model):
    annotator = models.ForeignKey('auth.User', to_field="id", related_name='annotations', on_delete=models.PROTECT)
    image = models.ForeignKey(Image, to_field="img_id", related_name='annotations', on_delete=models.PROTECT)
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
        fields = (
            'img_id', 'extension', 'img_path', 'user_id', 'sample_id',
            'eye', 'lens_type', 'nir_illumination', 'lens_brand', 'is_regular',
        )


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ('annotator', 'image', 'annotation', 'pk')


class UserSerializer(serializers.ModelSerializer):
    annotations = serializers.PrimaryKeyRelatedField(many=True, queryset=Annotation.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'annotations']
