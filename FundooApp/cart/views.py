import logging
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from bookstore.models import Book
from utility import token_required, decode_token
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Cart
from userlogin.models import User
from .serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated


class CartOperations(APIView):
    permission_classes = (IsAuthenticated,)
    logger = logging.getLogger(__name__)

    # @method_decorator(token_required)
    def post(self, request):
        try:
            # response = JWTAuthentication.authenticate(request=request.user)
            # print("HI")
            # if response is not None:
            #     user, token = response
            #     print("this is decoded token claims", token.payload)
            # else:
            #     print("token is missing")
            log_user = request.user
            # logging.info(log_user)
            print(log_user)
            user = User.objects.filter(id=log_user).first()
        except Exception as e:
            return Response({'message': str(e), 'status': 404})

        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            book_data = serializer.data['book']
            quantity = serializer.data['quantity']

            get_book = Book.objects.filter(id=book_data).first()
            if user and get_book:
                existing_item = Cart.objects.get(user=user, book=get_book, quantity=quantity)
                if existing_item:
                    print("HI")
                    existing_item.quantity += quantity
                    existing_item.save()
                else:
                    new_cart_item = Cart(user=user, book=get_book, quantity=quantity)
                    new_cart_item.save()

            return Response({"message": "cart item added", "status": 201})
        return Response({"message": serializer.errors, "status": 404})

    def delete(self, request, value):

        try:
            log_user = request.user.id
            user = User.objects.get(id=log_user)
            book = Book.objects.get(id=request.data['book_id'])
            cart_item = Cart.objects.get(id=request.data['cart_id'])
            cart = Cart.objects.get(id=cart_item.id, user=user, book=book.id)
        except Exception as e:
            return Response({'message': str(e), 'status': 404})

        # if removing an item where the quantity is 1, remove the cart item
        # completely otherwise decrease the quantity of the cart item
        if cart:
            if cart_item.quantity == 1:
                cart_item.delete()
            else:
                cart_item.quantity -= value
                cart_item.save()

            serializer = CartSerializer(cart_item)
            return Response({"message": "Quantity Updated", "status": 200})

    def get(self, request, value=None):
        if value:
            try:
                log_user = request.user.id
                user = User.objects.get(id=log_user)
                cart = Cart.objects.get(id=value, user=user)
            except Exception as e:
                return Response({"message": str(e), "status": 404})
            if cart:
                serializer = CartSerializer(cart)
                return Response({"message": "success", "data": serializer.data, "status": 200})

        cart = Cart.objects.all()
        serializer = CartSerializer(cart, many=True)
        return Response({"message": "success", "data": serializer.data, "status": 200})


class DeleteCart(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, id):
        try:
            log_user = request.user.id
        except Exception as e:
            return Response({"message": str(e), "status": 404})
        cart = get_object_or_404(Cart, user=log_user, id=id)
        cart.delete()

        return Response({"message": "Cart has been deleted", "status": 200})

