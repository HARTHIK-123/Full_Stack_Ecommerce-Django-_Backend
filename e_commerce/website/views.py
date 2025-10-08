from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from website.models import Products
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
import json


def home(request):
    products = Products.objects.all()
    context = {'products': products}
    return render(request,'website/index.html',context)



def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'website/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'website/login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

# def logout(request):
#     return render(request,'website/logout.html')


def dashboard(request):
    # your dashboard logic here
    return render(request, "website/dashboard.html") 

def user_list_view(request):
    users = User.objects.all()
    return render(request, "website/user_list.html", {"users": users})




def add_user_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if username and password and email:
            user = User.objects.create_user(username=username, email=email, password=password)
            # user.save()  # Not necessary if using create_user
            return redirect("user-list")
    return render(request, "website/add_user.html")


# ----------------- PRODUCT CRUD -----------------
@csrf_exempt
def product_list(request, pk=None):
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
        try:
            data = json.loads(request.body.decode("utf-8"))
            product = Products.objects.create(
                name=data["name"], description=data["description"], price=data["price"]
            )
            return JsonResponse({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    if request.method == "PUT" and pk:
        try:
            data = json.loads(request.body.decode("utf-8"))
            product = Products.objects.get(id=pk)
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
        except Products.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    if request.method == "DELETE" and pk:
        try:
            product = Products.objects.get(id=pk)
            product.delete()
            return JsonResponse({"message": "Deleted"}, status=200)
        except Products.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

    return JsonResponse({"error": "Method not allowed"}, status=405)


# ----------------- SIGNUP -----------------
@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        if not username or not password or not email:
            return JsonResponse({"error": "Username, email and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists!"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already in use!"}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        return JsonResponse({
            "success": True,
            "message": "User created successfully!",
            "username": user.username,
            "email": user.email
        }, status=201)

    return JsonResponse({"error": "Method not allowed"}, status=405)


# ----------------- LOGIN -----------------
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"success": False, "message": "Username and password required"}, status=400)

        user = authenticate(username=username, password=password)
        if user is not None:
            return JsonResponse({"success": True, "message": "Login successful"})
        else:
            return JsonResponse({"success": False, "message": "Invalid username or password"}, status=401)

    return JsonResponse({"error": "Method not allowed"}, status=405)


# -----------Users List----------
@csrf_exempt
def users_list(request):
    if request.method == "GET":
        users = list(User.objects.values("id", "username", "email"))
        return JsonResponse(users, safe=False)
    return JsonResponse({"error": "Method not allowed"}, status=405)