from django.db.models import Sum, F
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Order
from .serializer import OrderSerializer
from userlogin.models import User


class OrderViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    serializer = OrderSerializer

    def post(self, request):
        try:
            log_user = request.user.id
            user = User.objects.get(id=log_user)
        except Exception as e:
            return Response({"message": str(e), "status": 404})
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            cart = user.cart
            for cart_item in cart.all():
                if cart_item.book.quantity - cart_item.quantity < 0:
                    raise serializers.ValidationError(
                        'Does not have enough inventory of ' + str(cart_item.book.name) + 'in cart')

            # find the order total using the quantity of each cart item and the product's price
            total_aggregated_dict = cart.aggregate(
                total=Sum(F('quantity') * F('book__price')))

            order_total = round(total_aggregated_dict['total'], 2)
            order = serializer.save(total=order_total)

            order_items = []
            address = serializer.data['address']
            for cart_item in cart.all():
                order_items.append(Order(user=user, book=cart_item.book, quantity=cart_item.quantity, total=order_total,
                                         address=address, confirm_order=True))
                # available_inventory should decrement by the appropriate amount
                cart_item.book.quantity -= cart_item.quantity
                cart_item.book.save()

            Order.objects.bulk_create(order_items)
            return Response({"message": "Order is created", "status": 201})
        return Response({"message": serializer.errors, "status": 404})

    def get(self, id=None):

        if id:
            try:
                order = Order.objects.get(id=id)
            except Order.DoesNotExist:
                return Response({"message": "Cart Does not Exist", "status": 404})

            serializer = OrderSerializer(order)
            return Response({"message": "success", "data": serializer.data, "status": 200})

        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response({"message": "success", "data": serializer.data, "status": 200})
