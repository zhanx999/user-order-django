from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User,Order
# Create your views here.

@csrf_exempt
def users_api(request):

    if request.method =="GET":
        users = list(User.objects.values())
        return JsonResponse(users ,safe=False)
    
    elif request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        name = data.get('name')
        age = data.get('age')

        if not all([name,email,age]):
            return JsonResponse({'error': 'Missing fields'}, status=400)

        user = User.objects.create(name=name, email=email, age=age)
        return JsonResponse({'id': user.id, 'message': 'User created'}, status=201)
    

@csrf_exempt
def orders_api(request):
   
    if request.method == "GET":
        orders = list(Order.objects.values())
        return JsonResponse(orders,safe=False)

    elif request.method =="POST":
        data = json.loads(request.body)
        title = data.get('title')
        user_id = data.get('user_id')
        description = data.get('description')


        if not all([title, description, user_id]):
            return JsonResponse({'error': 'Missing fields'}, status=400)
        
        if not User.objects.filter(id=user_id).exists():
            return JsonResponse({'error': 'User not found'}, status=404)
        
        order = Order.objects.create(title=title,
                                      description=description,
                                        user_id=User.objects.get(id=user_id))
    
        return JsonResponse({'id':order.id,"message":"Order is created! :)"},status = 201)
  

@csrf_exempt
def order_api(request,order_id): #getById,putById,deleteById 
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    

    if request.method == "GET":
        return JsonResponse({"id":order.id,
                            'title': order.title,
                            'description': order.description,
                            'user_id': order.user.id})


    elif request.method =="PUT":
        data = json.loads(request.body)
        order.title = data.get('title',order.title)
        order.description = data.get('description',order.description)
        new_user_id = data.get('user_id')

        if new_user_id and not User.objects.filter(id=new_user_id).exists():
            return JsonResponse({'error': 'User not found'}, status=404)
        
        if new_user_id:
            order.user = User.objects.get(id=new_user_id)

        order.save()
        return JsonResponse({'message': 'Order updated successfully'})

    elif request.method =="DELETE":
        order.delete()
        return JsonResponse({'message': 'Order deleted'})


@csrf_exempt
def user_api(request,user_id): #getById,putById,deleteById 
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    if request.method == "GET":
        return JsonResponse({"id":user.id,
                            'name': user.name,
                            'email': user.email,
                            'age': user.age})

    
    elif request.method =="DELETE":
        user.delete()
        return JsonResponse({"message":"oops, user deleted"})
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.age = data.get('age', user.age)

        user.save()
        return JsonResponse({"message":"user updated "})
