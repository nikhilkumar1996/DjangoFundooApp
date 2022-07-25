import logging
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import Book
from rest_framework.response import Response
from .serializers import BookSerializer

logger = logging.getLogger(__name__)


class BookStore(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            logger.info("Book is Created")
            return Response({"message": "A Book entry is created", "status": 201})
        else:
            logger.error("Book is not created")
            return Response({"message": "error", "data": serializer.errors, "status": 400})

    def get(self, request, id=None):
        if id:
            try:
                book = Book.objects.get(id=id)
            except Book.DoesNotExist:
                return Response({"message": "Id Does not Exist", "status": 404})

            serializer = BookSerializer(book)
            logger.info("All Books are accessed")
            return Response({"message": "success", "data": serializer.data, "status": 200})

        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        logger.info("Book is accessed")
        return Response({"message": "success", "data": serializer.data, "status": 200})

    def patch(self, request, id):
        book = Book.objects.get(id=id)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.debug("Book is Updated")
            return Response({"message": "success", "status": 201})
        else:
            logger.warning("Error occurred while updating Book")
            return Response({"message": serializer.errors, "status": 404})

    def delete(self, request, id, number):
        book = get_object_or_404(Book, id=id)
        book.quantity = book.quantity - number
        book.save()

        logger.debug("Book is deleted")
        return Response({"message": "Book has been deleted", "status": 200})
