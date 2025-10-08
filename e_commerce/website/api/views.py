from django import http
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from website.api.serialization.product_serializer import ProductSerializer
from website.models import Products
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import json
from rest_framework.response import Response
from rest_framework import status

# ----------------- PRODUCT CRUD -----------------
@api_view(['GET'])
def product_list(request, pk=None):
    print("Product API called")
    serialized = ProductSerializer(Products.objects.all(), many=True)
    # return http.JsonResponse(serialized.data, safe=False)
    return Response(serialized.data)
    if request.method == "GET":
        if pk:
            try:
                product = Products.objects.get(id=pk)
                return JsonResponse({
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price
                })
            except Products.DoesNotExist:
                return JsonResponse({"error": "Product not found"}, status=404)
        products = list(Products.objects.values("id", "name", "description", "price"))
        return JsonResponse(products, safe=False)

    if request.method == "POST":
        data = json.loads(request.body)
        product = Products.objects.create(
            name=data["name"], description=data["description"], price=data["price"]
        )
        return JsonResponse({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price
        }, status=201)

    if request.method == "PUT" and pk:
        data = json.loads(request.body)
        try:
            product = Products.objects.get(id=pk)
        except Products.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

        product.name = data.get("name", product.name)
        product.description = data.get("description", product.description)
        product.price = data.get("price", product.price)
        product.save()
        return JsonResponse({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price
        })

    if request.method == "DELETE" and pk:
        try:
            product = Products.objects.get(id=pk)
        except Products.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

        product.delete()
        return JsonResponse({"message": "Deleted"}, status=204)



# ----------------- SIGNUP -----------------
@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")  # get email from request

        if not username or not password or not email:
            return JsonResponse({"error": "Username, email and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists!"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already in use!"}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        return JsonResponse({"success": True, "message": "User created successfully!", "username": user.username, "email": user.email}, status=201)



# ----------------- LOGIN -----------------
# @csrf_exempt
# def login_view(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         username = data.get("username")
#         password = data.get("password")
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except Exception:
            data = request.POST

        # Use get() for safety and default None
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"success": False, "message": "Username and password required"}, status=400)

        user = authenticate(username=username, password=password)
        if user is not None:
            return JsonResponse({"success": True, "message": "Login successful"})
        else:
            return JsonResponse({"success": False, "message": "Invalid username or password"}, status=401)




# -----------Users List----------
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
User = get_user_model()

User = get_user_model()

@csrf_exempt
def users_list(request):
    if request.method == "GET":
        users = User.objects.all().values("id", "username", "email")
        return JsonResponse(list(users), safe=False)
