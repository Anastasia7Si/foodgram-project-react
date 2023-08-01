from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserReadSerializer, FollowingSerializer
from .models import Following


User = get_user_model()


class UserViewSet(UserViewSet):
    """Вевьюсет пользователя."""
    queryset = User.objects.all()
    serializer_class = UserReadSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        context = {
            "request": request
        }

        if request.method == 'POST':
            serializer = FollowingSerializer(author,
                                             data=request.data,
                                             context=context)
            serializer.is_valid(raise_exception=True)
            Following.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            following = get_object_or_404(Following,
                                          user=user,
                                          author=author)
            following.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        context = {
            'request': request
        }
        pages = self.paginate_queryset(
            User.objects.filter(following__user=user))
        serializer = FollowingSerializer(pages,
                                         many=True,
                                         context=context)
        return self.get_paginated_response(serializer.data)
