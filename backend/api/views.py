from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.models import User

from rest_framework.decorators import permission_classes
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status

from .permissions import IsAnnotatorOwnerOrStaff
from .models import Annotation, AnnotationSerializer
from .models import Message, MessageSerializer
from .models import Image, ImageSerializer
from .models import UserSerializer


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
        print(" > Listing")
        serializer = ImageSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        print(" > Retrieving")
        image = get_object_or_404(self.queryset, imgID=pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    @permission_classes([ permissions.IsAdminUser ])
    def create(self, request):
        pass

    def patch(self, request, pk):
        pass


class UserList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAnnotatorOwnerOrStaff]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAnnotatorOwnerOrStaff]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AnnotationViewSet(viewsets.ViewSet):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAnnotatorOwnerOrStaff]
    queryset = Annotation.objects.all()
    http_method_names = ['get', 'post', 'head']

    def list(self, request):
        """Returns the list of annotations."""

        print(" > Listing")
        serializer = AnnotationSerializer(self.queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Returns the details of an annotation."""

        print(" > Retrieving: {}".format(pk))
        image = get_object_or_404(self.queryset, image=pk)
        serializer = AnnotationSerializer(image)
        return Response(serializer.data)

    # @action(detail=True, methods=['post'], name='Set Annotation')
    def create(self, request):
        """Create or update the annotation for an image."""

        print(request.data.keys())
        print(request.user.pk)
        # raise Exception("Whatever")

        img_instance = Image.objects.get(imgID=request.data['imgID'])
        # user_instance = User.object.get(pk=request.user.pk)

        ann = {
            'annotator': request.user,
            'image': img_instance,
        }
        print(ann)
        print("---------")
        annotation, _ = Annotation.objects.get_or_create({
            'annotator': request.user,
            'image': img_instance,
        })
        print(dir(annotation))
        annotation.annotation = request.data['annotation'] if 'annotation' in request.data else ""
        # serializer = AnnotationSerializer(annotation)
        try:
            annotation.full_clean()
            annotation.save()
            # headers = self.get_success_headers(annotation.data)
            print("New annotation stored.")
            return Response(
                {"Success": "annotation saved"},
                status=status.HTTP_201_CREATED,
                # headers=headers
            )
        except Exception as err:
            print(err)
            return Response(
                {"Fail": "annotation could NOT be saved"},
                status=status.HTTP_400_BAD_REQUEST
            )


# class AnnotationDetail(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAnnotatorOwnerOrStaff]
#     queryset = Annotation.objects.all()
