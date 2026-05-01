from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from profiles_api import serializer
from profiles_api import models
from profiles_api import permissions


class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializer.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""

        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})
    
    def post(self,request):
        """Create a hello message with our"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})
    
    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})
    
    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializer.HelloSerializer

    def list(self, request):
        """Return a hello message."""
        a_viewset =[
            "Uses actions (list, create, retrieve, update, partial_update)",
            "Automatically maps to URLs using Routers",
            "Provides more functionality with less code",
        ]
        return Response({'message':"Hello!", 'a_viewset': a_viewset})


    def create(self, request):
        """Create a new hello message."""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""

        return Response({'http_method': 'DELETE'})
    
class UserProfilesViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializer.UserProfileSerializer #Xác định serializer class cho viewset, trong trường hợp này là UserProfileSerializer. Serializer này sẽ được sử dụng để chuyển đổi dữ liệu giữa các đối tượng UserProfile và định dạng JSON khi gửi và nhận dữ liệu qua API.
    queryset = models.UserProfile.objects.all() #Lấy tất cả các đối tượng UserProfile từ cơ sở dữ liệu và gán cho queryset của viewset. Điều này cho phép viewset thực hiện các thao tác CRUD (Create, Read, Update, Delete) trên các đối tượng UserProfile thông qua API.
    authentication_classes = (TokenAuthentication,) #Xác định lớp xác thực cho viewset, trong trường hợp này là TokenAuthentication. Điều này có nghĩa là người dùng cần cung cấp một token hợp lệ để truy cập vào các endpoint của viewset này.
    permission_classes = (permissions.UpdateOwnProfile,) #Xác định lớp quyền hạn cho view
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializer.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permissions_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated
    )

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)