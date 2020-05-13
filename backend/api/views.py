from rest_framework.decorators import permission_classes
from django.views.decorators.cache import never_cache
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Message, MessageSerializer
from .models import Image, ImageSerializer

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ImageViewSet(viewsets.ViewSet):
    """
    API endpoint that allows images to be viewed and annotations stored.
    """

    queryset = Image.objects.all()

    def list(self, request):
        serializer = ImageSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):

        print(" > RETRIEVING")
        image = get_object_or_404(self.queryset, imgID=pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    @permission_classes([IsAdminUser])
    def create(self, request):
        print(" > CREATING")
        return Response()

    def patch(self, request, pk):
        print(" > PATCHING")
        # super.patch(request, imgID)
        image = get_object_or_404(self.queryset, imgID=pk)
        anns = image.annotations
        anns.extend(request.data['annotations'])
        # print(anns)
        serialized = ImageSerializer(image, data={'annotations': anns}, partial=True)
        serialized.is_valid()
        serialized.save()

        return Response()
