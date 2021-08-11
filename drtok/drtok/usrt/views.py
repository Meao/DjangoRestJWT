from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import ReadOnlyUserSerializer, WriteOnlyUserSerializer

@api_view(['GET','POST'])
def register(request):
    if request.method == 'POST':
        serializer=WriteOnlyUserSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data['username']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            is_active = request.data['is_active']
            password = request.data['password']
            password2 = request.data['confirm']
            if password == password2:
                if User.objects.filter(username=username).exists():
                    return Response('User with same username already exists',status=status.HTTP_403_FORBIDDEN)
                else:
                    user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, is_active=is_active)
                    user.save()
                    return Response('User Registered successfully',status=status.HTTP_201_CREATED)
            else:
                return Response('Password and Confirm Password do not match',status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(f"Welcome.")

@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def profile(request):
    try:
        user = User.objects.get(id=request.user.id)
        if request.method == 'GET':
            serializer = ReadOnlyUserSerializer(user)
            return Response(serializer.data,status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            serializer=WriteOnlyUserSerializer(data=request.data)
            if serializer.is_valid():
                user.username = request.data['username']
                user.first_name = request.data['first_name']
                user.last_name = request.data['last_name']
                user.is_active = request.data['is_active']
                user.password = request.data['password']
                user.save()
                return Response('User updated successfully',status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        if request.method == 'DELETE':
            serializer=WriteOnlyUserSerializer(data=request.data)
            if serializer.is_valid():
                user.is_active = False
                user.save()
                return Response('User deleted successfully',status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET','POST'])
def login(request):
    if request.method == 'GET':  
        return Response('WELCOME. Enter your login credentials(username and password)')
    else:    
        username = request.data['username']
        password = request.data['password']
        
        if User.objects.filter(username=username).exists()==False:
            return Response('User does not exist',status=status.HTTP_404_NOT_FOUND)        
        else:
            user = authenticate(username=username, password=password) 
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },status=status.HTTP_200_OK)
            else:                       
                return Response('Username or Password is incorrect',status=status.HTTP_401_UNAUTHORIZED)   

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def BlacklistTokenView(request):
    if request.method=='POST':
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response('Logged Out',status=status.HTTP_200_OK)
        except Exception as e:
            print(Exception)
            return Response('Exception',status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# from django.contrib.auth.models import User
# # from rest_framework import viewsets
# from rest_framework import permissions
# from rest_framework import status
# from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.response import Response
# # from rest_framework.views import APIView
# from . import serializers
# # from .serializers import UserSerializer
# from django.contrib.auth.models import User

# class ListUsers(ListAPIView):
#     """
#     View to list all users in the system.
#     * Only admin users are able to access this view.
#     """
#     # authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser]
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = serializers.ReadOnlyUserSerializer

#     # def get(self, request, format=None):
#     #     """
#     #     Return a list of all users.
#     #     """
#     #     usernames = [user.username for user in User.objects.all()]
#     #     return Response(usernames)

# class UserAPI(ListCreateAPIView):
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = serializers.WriteOnlyUserSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response({"status": True,
#                          "message": "User added ",
#                          "data": serializer.data},
#                         status=status.HTTP_201_CREATED, headers=headers)


# class UserRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
#     serializer_class = serializers.WriteOnlyUserSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return User.objects.filter(id=self.kwargs.get('pk', None))

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, 
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}

#         return Response({"status": True, "message": "User updated ", "data": serializer.data})



# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]