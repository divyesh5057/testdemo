from django.shortcuts import render
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from account.models import *
import requests
from django.core.paginator import Paginator
from account.models import *
from django.db.models import Q
from account.serializers import * 
from django.core import serializers
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# def home(request):
#     return render(request, 'login.html')

# @login_required
def Login(request):
    
    if request.method != "POST":
        return render(request,"login.html")
    
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")


        url = 'http://0.0.0.0:8980/login/'
        data = {
            'username': username,
            'password': password,
        }
        headers = {
            # 'Content-Type': 'application/json',
            # 'Authorization': 'Token 11b79bad0061bfce54de464fd34ff7934d12f2fc',
        }

        response = requests.post(url, json=data, headers=headers)
        data = response.json()
        if response.status_code == 200:
            user_id = data['user_id']
            print(user_id)

            user = User.objects.get(id=user_id)
            is_admin = user.is_staff
        
        print(data,">>>>>>>>>>..............")



    if response.status_code == 200 and is_admin : 
        access_token= data['token']
        request.session['access_token'] = access_token
        request.session['username'] = username
        request.session['password'] = password
        
        return redirect("frontend:dashboard")
    

        # Handle successful response
        pass
    elif response.status_code == 404:
        messages.error(request,"Data is not valid. Please try again",extra_tags="error")
    else:
        # Handle error response
        pass
   
    messages.error(request,"Data is not valid. Please try again",extra_tags="error")
    return redirect("frontend:login")

def Dashboard(request):
    total_category = Category_db.objects.all().count()
    total_banner = banner_db.objects.all().count()
    total_user = User.objects.all().count()

    print(total_category,total_banner,total_user,">><<<<<")
    # if "id" not in request.session or "email" not in request.session or "type" not in request.session:
    #     messages.error(request,"Login first and then try again",extra_tags="error")
    context = {"total_category":total_category,"total_banner":total_banner,"total_user":total_user}
    return render(request,"userpages/dashboard.html",context)

def Logout(request):
    access_token = request.session.get('access_token', None)
    username = request.session.get('username', None)
    password = request.session.get('password', None)

    print(username,password,"<><><><>")

    url = 'http://0.0.0.0:8980/logout/'
    data = {
        "username":username,
        "password":password
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {access_token}',
    }

    response = requests.post(url, json=data, headers=headers)
    request.session.clear()
    return redirect("frontend:login")

def ShowProject(request):
    url = 'http://0.0.0.0:8980/category/'
    access_token = request.session.get('access_token', None) 
    data = {
       
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {access_token}',
    }

    response = requests.get(url, json=data, headers=headers)
    if 'q' in request.GET:
        q = request.GET['q']
        print("i am in q",q)
        all_project_data = Category_db.objects.filter(name__icontains=q)
        print("all_project_data",all_project_data)
        # return redirect("frontend:showproject")
    # if response.status_code == 200:
    #     response_data = response.json()
    #     all_project_data = response_data['results']
    else:
        # pass
        # response_data = response.json()
        # all_project_data = response_data['results']
        all_project_data = Category_db.objects.all()

    
    paginator=Paginator(all_project_data,5)
    page_number = request.GET.get('page')
    obj_data = paginator.get_page(page_number)
    totalpage = obj_data.paginator.num_pages
    context ={"all_project_data":obj_data,"lastpage":totalpage,"totalpagenumber":[n+1 for n in range(totalpage)]}
    return render(request,"userpages/showproject.html",context)

def search_view(request):
    # Get search parameters from request
    search_term = request.GET.get('q')
    
    # Query the database for products matching the search term
    products = Category_db.objects.filter(name__icontains=search_term)
    
    # Serialize the search results into JSON
    # serializer = CategorySerializer(products)
    # user = User.objects.get(id=user_id)
    # serializer = UserProfileSerializer(user)
    # return Response(serializer.data,status=200)
    data = serializers.serialize('json', products)
    # Return the search results as JSON response
    return JsonResponse(data, safe=False)


def AddProject(request,id=0):
    name = request.GET.get('name', '')
    access_token = request.session.get('access_token', None) 
    print("~~~~~~~~~~~~~~>>>>>>",id)
    
    if id==0:
        if request.method == "POST":

            name = request.POST.get("name")
    

            url = 'http://0.0.0.0:8980/category/'
            data = {
                'name': name,
            }
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Token {access_token}',
            }

            response = requests.post(url, json=data, headers=headers)
            all_project_data = response.json()
            # print(response,"~~~~~~~~~~~~~")
            messages.success(request,"Data added.",extra_tags="success")
            return redirect("frontend:showproject")
        
    else:
       

        if request.method == "POST":
            name = request.POST.get("name")
            url = f'http://0.0.0.0:8980/category/{id}/'
            data = {
                'name': name,
            }
            headers = {
                'Content-Type': 'application/json',
               'Authorization': f'Token {access_token}',
            }
            response = requests.put(url, json=data, headers=headers)
            messages.success(request,"Data Update.",extra_tags="success")
            update_data = response.json()
            return redirect("frontend:showproject")
        context = {"id":id,"name":name}
        return render(request,"userpages/addproject.html",context)

    return render(request,"userpages/addproject.html")

def Updateproject(request,id=0):

    print(id,"~~~~~~~~~~~~~~>>>>>>")
    return render(request,"userpages/showproject.html")

def DeleteProject(request,id):
    access_token = request.session.get('access_token', None) 
    url = f'http://0.0.0.0:8980/category/{id}/'
    data = {

    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {access_token}',
    }

    response = requests.delete(url, json=data, headers=headers)

    messages.success(request,"Your file has been deleted.",extra_tags="deletesuccess")
    return redirect("frontend:showproject")

def ShowTask(request):

    obj = banner_db.objects.all()
    access_token = request.session.get('access_token', None) 
    url = 'http://0.0.0.0:8980/get_all_banners/'
    data = {
       
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {access_token}',
    }

    response = requests.get(url, json=data, headers=headers)
    all_task_data = response.json()
    d = all_task_data['data']
    # for i in d:
    # print(all_task_data['data'])
    my_list = all_task_data['data']
    templates_string = ''
    for dictionary in my_list:
        if dictionary.get('templates'):
            # print("i am for >>>>>",dictionary['templates'])
            templates_string += ', '.join(dictionary['templates'])


    obj = banner_db.objects.all()
    category_ids = [item.category_id for item in obj]
    unique_category_ids = list(set(category_ids))
    category_names = [Category_db.objects.get(id=id).name for id in unique_category_ids]
    print(category_names,"????????????????")
    if 'q' in request.GET:
        query = request.GET['q']
        # query = "demo" # replace with your search query
        category_names = [name for name in category_names if query.lower() in name.lower()]

    paginator=Paginator(category_names,5)
    page_number = request.GET.get('page')
    obj_data = paginator.get_page(page_number)
    totalpage = obj_data.paginator.num_pages
    context ={"all_task_data":obj_data,"lastpage":totalpage,"totalpagenumber":[n+1 for n in range(totalpage)]}
    return render(request,"userpages/showtask.html",context)

def AddTask(request,pk=0):
    obj = Category_db.objects.all()
    
    if request.method == "POST":
        category = request.POST.get('category_id')
        banner = request.FILES.get('banner_img')
        print("KJJJJJJJJJJJJJJJJJJJ",category)
        banner_obj = banner_db(banner_img=banner,category_id =category)
        banner_obj.save()
       
        messages.success(request,"Data added.",extra_tags="success")
        
        return redirect("frontend:showtask")
        
    
    context ={"all_task_data":obj}
    return render(request,"userpages/addtask.html",context)

def All_imgage(request, id=0):

    name = request.GET.get('id')
    
    if id !=0:
        banner_obj = banner_db.objects.get(id=id)
        print(banner_obj.category_id,">>>>>>>>>>>>>>>>>>>>>>>>")
        obj = Category_db.objects.filter(id=banner_obj.category_id).all()
        if request.method == "POST":
            category = request.POST.get('category_id')
            banner = request.FILES.get('banner_img')
            banner_obj.category_id = category
            banner_obj.banner_img = banner
            banner_obj.save()
            messages.success(request,"Data Update.",extra_tags="success")
            return redirect("frontend:showtask")
        context ={"id":banner_obj.category_id,"banner_img":banner_obj.banner_img,"all_task_data":obj}

        return render(request,"userpages/addtask.html",context)
    else:
        # if request.method == "POST":
        obj1 = Category_db.objects.get(name=name).id
        obj = banner_db.objects.filter(category_id = obj1).all()  
        access_token = request.session.get('access_token', None) 
        id_ = int(obj1)
        url = f'http://0.0.0.0:8980/category_banners/{id_}'
        data = {
        
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {access_token}',
        }
        response = requests.get(url, json=data, headers=headers)
        result = response.json()
        data = result['results']
        context ={"all_task_data":obj,"data":data}

    return render(request,"userpages/banner.html",context)

def DeleteImage(request,id):
    access_token = request.session.get('access_token', None) 
    url = f'http://0.0.0.0:8980/delete_banner/{id}/'
    data = {

    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {access_token}',
    }

    response = requests.delete(url, json=data, headers=headers)

    messages.success(request,"Your imgage has been deleted.",extra_tags="deletesuccess")
    return redirect("frontend:showtask")


def UserProfile(request):
    access_token = request.session.get('access_token', None) 
    url = 'http://0.0.0.0:8980/user-profile/'
    data = {
       
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {access_token}',
    }

    response = requests.get(url, json=data, headers=headers)
    list1 = []
    all_task_data = response.json()
    list1.append(all_task_data)
    print(list1,"~~~~~~~~~~")
    for i in all_task_data:
        profilei_image = i.profilei_image
        email = i.email
        phone_number = i.phone_number
        full_name = i.full_name
        designation = i.designation
    context ={"all_task_data":all_task_data}
    return render(request,"userpages/profile.html",context)

def ShowEmployee(request):
    access_token = request.session.get('access_token', None) 
    url = 'http://0.0.0.0:8980/getalluser/'
    data = {
       
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {access_token}',
    }

    response = requests.get(url, json=data, headers=headers)
    all_emp_data = response.json()
    print(all_emp_data,"")
    if 'q' in request.GET:
        query = request.GET['q']
        all_emp_data = [item for item in all_emp_data if (query in item.get('username', '') or query in item.get('email', '') or query in str(item.get('phone_number', '')))]
    paginator=Paginator(all_emp_data,5)
    page_number = request.GET.get('page')
    obj_data = paginator.get_page(page_number)
    totalpage = obj_data.paginator.num_pages
    context ={"all_emp_data":obj_data,"lastpage":totalpage,"totalpagenumber":[n+1 for n in range(totalpage)]}
    # context ={"all_emp_data":all_emp_data}

    return render(request,"userpages/showemployee.html",context)

def AddEmployee(request,id=0):
    name = request.GET.get("username")
    email_id = request.GET.get("email")
    mobile = request.GET.get("mobile")
    access_token = request.session.get('access_token', None) 
    
    if id==0:
        print("i am if >>>>>>>>>>>>")

        if request.method == "POST":
            username = request.POST.get('username', '')
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            password2 = request.POST.get('password2', '')
            phone_number = request.POST.get('phone_number', '')
            user_type  = request.POST.get('emp_type')
            name = request.POST.get("name")
    
            print(user_type,">>>>>><<<<<<<<<>>>><<<>><<><<><><><><>")
            url = 'http://0.0.0.0:8980/register/'
            data = {
                    "username":username,
                    "email": email,
                    "password": password,
                    "password2":password2,
                    "phone_number":phone_number,
                    "is_admin":user_type
            }
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Token {access_token}',
            }

            response = requests.post(url, json=data, headers=headers)
            all_project_data = response.json()
            messages.success(request,"Data added.",extra_tags="success")
            return redirect("frontend:showemployee")
        
    else:
        data=User.objects.get(pk=id)
        if request.method == "POST":
            username = request.POST.get('username', '')
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            password2 = request.POST.get('password2', '')
            phone_number = request.POST.get('phone_number', '')
            user_type  = request.POST.get('emp_type')

            url = f'http://0.0.0.0:8980/updateuser/{id}/'

            data = {
                "username":username,
                "email": email,
                "password": password,
                "password2":password2,
                "phone_number":phone_number,
                "is_admin":user_type
            }

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Token {access_token}',
            }
            response = requests.put(url, json=data, headers=headers)
            messages.success(request,"Data Update.",extra_tags="success")
            return redirect("frontend:showemployee")
        context = {"id":id,"data":data}
        return render(request,"userpages/addemployee.html",context)

    return render(request,"userpages/addemployee.html")

def DeleteEmployee(request,id):
    access_token = request.session.get('access_token', None) 
    url = f'http://0.0.0.0:8980/deleteuser/{id}/'
    data = {

    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {access_token}',
    }

    response = requests.delete(url, json=data, headers=headers)

    messages.success(request,"User has been deleted.",extra_tags="deletesuccess")

    return redirect("frontend:showemployee")

