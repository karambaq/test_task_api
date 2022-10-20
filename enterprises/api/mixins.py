from rest_framework import viewsets, mixins, permissions


class ListRetrieveViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
