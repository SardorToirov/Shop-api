from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import ProductViewHistorySerializer
from drf_spectacular.utils import extend_schema


class ProductViewHistoryCreated(APIView):
    serializer_class = ProductViewHistorySerializer

    @extend_schema(
        summary="Product view history yaratish",
        tags=["ProductViewHistory"]
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
