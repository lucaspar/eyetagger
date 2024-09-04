import random

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from .models import (
    Annotation,
    AnnotationSerializer,
    Image,
    ImageSerializer,
    Message,
    MessageSerializer,
    Profile,
    ProfileSerializer,
    UserSerializer,
)
from .permissions import IsAnnotatorOwnerOrStaff

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name="index.html"))


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ["get", "patch"]

    @permission_classes([permissions.IsAdminUser])
    def patch(self, request, pk):
        testmodel_object = self.get_object(pk)
        serializer = serializer_class(
            testmodel_object,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(code=201, data=serializer.data)
        return JsonResponse(code=400, data="Invalid parameters")


class ImageViewSet(viewsets.ViewSet):
    """
    API endpoint that allows images to be viewed.
    """

    queryset = Image.objects.all()

    def list(self, request):
        print(" > Listing")
        MAX_ITEMS_TO_RETURN = 100

        # filter and sort images by id
        response_set = self.queryset.filter(lens_type="F")  # return only "fake" lenses
        response_set = response_set.order_by("img_id")

        # exclude the images already annotated by valid (non-test) users
        annotations = Annotation.objects.all()
        annotator_users = [x.annotator for x in annotations]
        valid_profiles = Profile.objects.filter(is_test=False).filter(
            user__in=annotator_users
        )
        valid_users = [p.user for p in valid_profiles]
        valid_annotated_img = [
            x.image.img_id for x in annotations if x.annotator in valid_users
        ]
        response_set = response_set.exclude(img_id__in=valid_annotated_img)
        print(f"Remaining images: {response_set.count()}")

        # shuffle and cap to maximum number
        response_set = sorted(response_set, key=lambda x: random.random())
        response_set = response_set[:MAX_ITEMS_TO_RETURN]

        # send to client
        serializer = ImageSerializer(response_set, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        print(" > Retrieving")
        image = get_object_or_404(self.queryset, img_id=pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    @permission_classes([permissions.IsAdminUser])
    def create(self, request):
        pass

    @permission_classes([permissions.IsAdminUser])
    def patch(self, request, pk):
        pass


class UserList(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAnnotatorOwnerOrStaff,
    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAnnotatorOwnerOrStaff,
    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AnnotationViewSet(viewsets.ViewSet):
    queryset = Annotation.objects.all()
    http_method_names = ["get", "post", "head"]

    def list(self, request):
        """Returns the list of annotations."""

        print(f" > Listing: {self.queryset.count()}")
        serializer = AnnotationSerializer(
            self.queryset, context={"request": request}, many=True
        )
        return Response(serializer.data)

    @permission_classes([IsAnnotatorOwnerOrStaff])
    def retrieve(self, request, pk):
        """Returns the details of an annotation."""

        print(f" > Retrieving: {pk}")
        image = get_object_or_404(self.queryset, image=pk)
        serializer = AnnotationSerializer(image)
        return Response(serializer.data)

    def create(self, request):
        """Create or update the annotation for an image."""

        print(f"User {request.user.pk} posting new annotations.")

        failures = list()
        successes = list()
        print(len(request.data))
        for ann in request.data:
            img_instance = Image.objects.get(img_id=ann["img_id"])
            annotation, _ = Annotation.objects.get_or_create(
                annotator=request.user,
                image=img_instance,
            )
            annotation.annotation = ann["annotation"] if "annotation" in ann else ""
            try:
                response = annotation.save()
                print(
                    "New annotation stored: {} -- {} :: {}".format(
                        response, annotation.id, ann["img_id"]
                    )
                )
                successes.append(img_instance.img_id)
            except Exception as err:
                failures.append(img_instance.img_id)
                print(f"Failed to store annoration: {err}")

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
            status=status.HTTP_400_BAD_REQUEST,
        )
