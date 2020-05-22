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
        MAX_ITEMS_TO_RETURN = 5

        filtered_set = self.queryset.filter(lens_type="F")  # return only "fake" lenses
        filtered_set = filtered_set.order_by('img_id')
        filtered_set = filtered_set[:MAX_ITEMS_TO_RETURN]

        serializer = ImageSerializer(filtered_set, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        print(" > Retrieving")
        image = get_object_or_404(self.queryset, img_id=pk)
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

    # TODO: make a proper front-end login and uncomment the line below
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAnnotatorOwnerOrStaff]
    queryset = Annotation.objects.all()
    http_method_names = ['get', 'post', 'head']

    def list(self, request):
        """Returns the list of annotations."""

        print(" > Listing: {}".format(len(self.queryset)))
        serializer = AnnotationSerializer(self.queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Returns the details of an annotation."""

        print(" > Retrieving: {}".format(pk))
        image = get_object_or_404(self.queryset, image=pk)
        serializer = AnnotationSerializer(image)
        return Response(serializer.data)


    def create(self, request):
        """Create or update the annotation for an image."""

        print("User {} posting new annotations.".format(request.user.pk))

        failures = list()
        successes = list()
        print(len(request.data))
        for ann in request.data:

            img_instance = Image.objects.get(img_id=ann['img_id'])
            annotation, _ = Annotation.objects.get_or_create(
                annotator=request.user,
                image=img_instance,
            )
            # print(ann['annotation'])
            annotation.annotation = ann['annotation'] if 'annotation' in ann else ""
            try:
                response = annotation.save()
                print("New annotation stored: {} -- {} :: {}".format(
                    response, annotation.id, ann['img_id']))
                successes.append(img_instance.img_id)
            except Exception as err:
                failures.append(img_instance.img_id)
                print("Failed to store annoration: {}".format(err))

        if len(failures) == 0:
            return Response(
                {
                    "message": "all annotations saved",
                    "success": True,
                    "successes": successes,
                    "failures": failures,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "message": "some annotations could NOT be saved.",
                "success": False,
                "successes": successes,
                "failures": failures,
            },
            status=status.HTTP_400_BAD_REQUEST
        )


# class AnnotationDetail(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAnnotatorOwnerOrStaff]
#     queryset = Annotation.objects.all()
