from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import * 
from django.contrib.auth import authenticate, logout
from account.models import User,banner_db,Category_db,AdminBanners
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.viewsets import ModelViewSet
from account.helpers import send_otp_via_email,IsAuthenticatedOrCreate,PermissionPolicyMixin,Custom_Pagination
from rest_framework import generics
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.core.cache import cache   

# Create your views here.


class UserRegistrationView(APIView):
    """
       An endpoint for  Register User
    """
    def post(self, request, format=None):
        # try:
        email = request.data.get('email')
        if email:
            
            user = User.objects.filter(email=email)
            
            if user.exists():
                return Response({'status': False, 'detail': 'Email is already exists'})

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            
            data=send_otp_via_email(email)
            
            user=serializer.save()
            user.otp=data
            user.save()
            response={
                'msg':'Registration Success',
                'status':True,
                'data':serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # except Exception:
        #     response={
        #             'msg':'Something went wrong',
        #             'status':False,
        #         }
        #     return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self,request,format=None):
        try:
            user = User.objects.all()
            serializer = UserRSerializer(user,many=True)
            print(user)
            return Response(serializer.data,status=200)
        except Exception:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ValidateOTP(APIView):
    """
        An endpoint for Validate OTP  From Email To verify User
    """
    def post(self, request, *args, **kwargs):
        try:
            email = request.data .get('email', False)
            otp_send = request.data.get('otp', False)
           
            if email and otp_send:
                old = User.objects.get(email=email)
                if old:
                    otp = old.otp
                    if str(otp_send) == str(otp):
                        old.validated = True
                        old.save()
                        
                        token = Token.objects.get_or_create(user=old)[0].key
                       
                        return Response({'token':token,'status': True, 'detail' : "OTP matched."})
                    
                    else:
                        return Response({'status': False, 'detail': 'OTP incoorect'})            
            
            
                else:
                    return Response({'status': False, 'detail' : "First proceed via sending otp request"})
            
                
            else:
                return Response({'status': False, 'detail' : "Please provide both email and otp for validation"})
        except Exception as e:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(APIView):
    """
        An endpoint for UserLogin
    """
    def post(self, request, format=None):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                username = serializer.data.get('username')
                password = serializer.data.get('password')
                user = authenticate(username=username, password=password)
                token = Token.objects.get_or_create(user=user)[0].key
                if user is not None:
                    return Response({'token':token,'user_id':user.id,'msg':'Login Success'}, status=status.HTTP_200_OK)
                else:
                    return Response({'errors':{'non_field_errors':['username or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        except Exception as e:
            return Response({'errors':{'non_field_errors':['username or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
    
    
class UserLogoutView(APIView):
    """ 
      An endpoint for  User Logout 
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        try:
            request.user.auth_token.delete()
            logout(request)
            return Response({'mag':'User Logged out successfully','status':True,},status=status.HTTP_200_OK)
        except Exception:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class UserRetrieveUpdateDestroyAPIView(APIView): 
    """ 
       An endpoint for User Retrieve,Update and Delete 
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request,id):
        try:
            user = User.objects.get(id=id)
            serializer = UserRegistrationSerializer(user)
            return Response(serializer.data,status=200)
        except :
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request,id):
        user = User.objects.get(id=id)
        data=request.data
        serializer = UserSerializer(user,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self,request,id,format=None):
        try:
            user = User.objects.get(id=id) 
            user.delete()
            return Response({"msg":" User deleted successfully ","status":True})
        except:
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(APIView): 
    """ 
       An endpoint for User Retrieve,Update and Delete 
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]  
    def get(self,request):
        try:
            user_id=request.user.id
            
            user = User.objects.get(id=user_id)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data,status=200)
        except Exception:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request,):
        try:
            user_id=request.user.id
            user = User.objects.get(id=user_id)
            data=request.data
            serializer = UserProfileSerializer(user,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
        
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
 
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': True,
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ResendUserOtpAPIView(APIView):
    """
        An endpoint for ResendOTP its also Useful in Forgot Aassword Api
    """
    def post(self,request):
        try: 
            email = request.data.get('email')
            user = User.objects.get(email=email)
            
            if user:
                data=send_otp_via_email(user.email)
                user.otp=data
                user.save()
                response={
                            'msg':'OTP send successfully',
                            'status':True,
                            'OTP':data
                        }
                return Response(response, status=status.HTTP_201_CREATED)
            response={
                        'msg':'Email is Not Validate',
                        'status':False,
                    }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    


class ResetPasswordAPIView(APIView):
    """
        An endpoint For ForgotPassword or ResetPassword 
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def patch(self,request):
        try:
            user=request.user.id
            user = User.objects.get(id=user)
            if user:
                serializer = ResetPasswordSerializer(user,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response = {
                    'status': True,
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                }
                    return Response(response)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except :
            return Response ({"msg":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class CategoryModelViewSet(ModelViewSet):    
#     """
#       An endpoint for  Category CRUD 
#     """
#     # authentication_classes=[TokenAuthentication]
#     # permission_classes=[IsAuthenticated]
#     # permission_classes_per_method = {
#     #     "list": [IsAuthenticated],
#     #     "retrieve": [IsAuthenticated],
#     #     "create": [IsAuthenticated,IsAuthenticatedOrCreate],
#     #     "update": [IsAuthenticated,IsAuthenticatedOrCreate]
#     # }
#     serializer_class = CategorySerializer
#     queryset = Category_db.objects.all()


class BanerAPIView(APIView):
    """
        An endpoint for Get and Add banner 
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        user = banner_db.objects.all()
        category=Category_db.objects.all()
        list_of_data=[]
        for i in category:
            di={}
            li=[]
            di['category_name']=i.name
            for j in user:
                if i.id==j.category.id:
                    li.append(j.banner_img.url)
            di['templates']=li
            list_of_data.append(di)
        response = {
                'status': True,
                'code': status.HTTP_200_OK,
                'data': list_of_data,
            }
        return Response(response)
    
    def post(self,request):
        try:
            if request.user.is_admin==True:
                seralizer=BanerSerializers(data=request.data)
                if seralizer.is_valid(raise_exception=True):
                    seralizer.save()
                    response={
                        'status':True,
                        'msg':"Banner added successfully",
                        'data':seralizer.data
                    }
                    return Response(response,status=status.HTTP_201_CREATED)
                response={
                        'msg':"Something went wrong",
                        'status':False,
                        'data':None
                    }    
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                response = {
                        'status': False,
                        'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                        'msg': "NON_AUTHORITATIVE_INFORMATION",
                    }  
                return response
        except :
            return Response ({"msg":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BannerRetrieveUpdateDestroyAPIView(APIView):
    """
        An endpoint for  Retrieve,Update and Destroy Banners/templates
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request,id,):
        try:
            user = banner_db.objects.get(id=id)
            serializer = BanerSerializers(user)
            return Response(serializer.data,status=200)
        except :
            return Response ({"msg":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request,id,):
        try:
            if request.user.is_admin==True:
                user = banner_db.objects.get(id=id)
                serializer = BanerSerializers(user,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors)
            else:
                    response = {
                            'status': False,
                            'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                            'msg': "NON_AUTHORITATIVE_INFORMATION",
                        }  
                    return response
        except :
            return Response ({"msg":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request,id,format=None):
        try:
            if request.user.is_admin==True:
                banner_obj = banner_db.objects.get(id=id) 
                banner_obj.delete()
                return Response({"msg":" Banner deleted successfully "})
            else:
                response = {
                        'status': False,
                        'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                        'msg': "NON_AUTHORITATIVE_INFORMATION",
                    }  
                return response
        except :
            return Response ({"msg":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
# class GetCategoryBanners(APIView):
#     """ 
#       An endpoint for  get all templates for specif categorys
#     """
#     def get(self,request,category_id):
#         try:
#             banner_obj = banner_db.objects.filter(category__id=category_id).all()
#             serializer = BanerSerializers(banner_obj,many=True)
#             return Response(serializer.data,status=200)
#         except :
#             return Response ({"msg":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class AdminBannerModelViewSet(PermissionPolicyMixin,ModelViewSet):
    """
        An endpoint for admin banners/templates
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated,IsAuthenticatedOrCreate],
        "update": [IsAuthenticated,IsAuthenticatedOrCreate]
    }
    serializer_class = AdminBannersSerializer
    queryset = AdminBanners.objects.all()
    def destroy(self, request, *args, **kwargs):
        try:
            if request.user.is_admin==True:
                # do your customization here
                user_object = self.get_object()
                AdminBanners.objects.filter(id=user_object.id).delete()
                user_object.delete()
                response={
                    "msg":"banner deleted successfully",
                    "status":True
                }
                return Response(response,status=status.HTTP_204_NO_CONTENT)
            else:
                response = {
                        'status': False,
                        'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                        'msg': "NON_AUTHORITATIVE_INFORMATION",
                    }  
                return Response(response,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except :
            return Response (status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    
class CategoryModelViewSet(ModelViewSet):    
    """
      An endpoint for  Category CRUD 
    """
    serializer_class = CategorySerializer
    queryset = Category_db.objects.all()
    pagination_class = Custom_Pagination
    def list(self, request,  *args, **kwargs):
        paginator = self.pagination_class()
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(page, many=True)
        response_data = paginator.get_paginated_response(serializer.data)
        # cache.set(cache_id, response_data,timeout_in_seconds)
        return Response(response_data)
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated,IsAuthenticatedOrCreate],
        "update": [IsAuthenticated,IsAuthenticatedOrCreate]
    }
    
class GetCategoryBanners(APIView):
    pagination_class = Custom_Pagination  # Use the custom pagination class
    def get(self, request,category_id):
        timeout_in_seconds = 10 * 86400
        # Check if the results are already in the cache
        cache_id=f"id_{category_id}_1"
        cached_data = cache.get(cache_id)
        if cached_data is not None:
            return Response(cached_data)
        results =  banner_db.objects.filter(category__id=category_id).all()
        # Paginate the results and return the current page
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(results, request)
        serializer = BanerSerializers(page, many=True)
        response_data = paginator.get_paginated_response(serializer.data)
        
        # cache.set(cache_id, response_data,timeout_in_seconds)
        return Response(response_data)