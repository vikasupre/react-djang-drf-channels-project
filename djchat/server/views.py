from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from .models import Server, Channel, Category
from .serializer import ServerSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count
from .schema import server_list_docs


# Define a viewset for handling server-related operations
class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()  # Queryset for retrieving Server objects

    # Define a method to handle list requests
    @server_list_docs
    def list(self, request):
        """List servers based on query parameters.

        This view retrieves a list of servers based on the provided query parameters. The available query parameters
        include:

        Args:
            request (HttpRequest): The HTTP request object.

        Query Parameters:
        - category (str, optional): Filter servers by category.
        - qty (int, optional): Limit the number of servers returned.
        - by_user (bool, optional): Filter servers by user membership.
        - by_serverid (int, optional): Filter servers by server ID.
        - with_num_members (bool, optional): Include the number of members in the response.

        Raises:
            AuthenticationFailed: If the user is not authenticated and tries to filter by user or server ID.
            ValidationError: If the provided server ID does not exist or if the server ID is not a valid integer.

        Returns:
            Response: A list of server objects based on the query parameters.

        Example:
        To retrive all servers in the 'gameing' category with atleast 5 members you can make following request:

            GET /api/servers/?category=gaming&with_num_members=true&num_members__gte=5

        To retrieve servers in a specific category:

            GET /api/servers/?category=gaming

        To limit the response to 5 servers:

            GET /api/servers/?qty=5

        To include the number of members in the response:

            GET /api/servers/?with_num_members=true
        To retrieve servers with serverid:

            GET /api/servers/?by_serverid=1

        """

        # Retrieve query parameters from the request
        category = self.request.query_params.get('category')
        qty = self.request.query_params.get('qty')
        by_user = self.request.query_params.get('by_user') == 'true'
        by_serverid = self.request.query_params.get('by_serverid')
        with_num_members = self.request.query_params.get(
            'with_num_members') == 'true'


        # if by_user or by_serverid id True and user is no authenticated then raise AuthenticationFailed error
        if (by_user or by_serverid) and not request.user.is_authenticated:
            print('by_user11', by_user)
            print('user', request.user)
            raise AuthenticationFailed()

        # Filter queryset by category_name if provided
        if category:
            self.queryset = self.queryset.filter(category__name=category)
            print('queryset', self.queryset)

        # Filter queryset by user if 'by_user' is True
        if by_user:
            user_id = request.user.id
            print('user_id', user_id)
            self.queryset = self.queryset.filter(member=user_id)

        # Annotate queryset with member count if 'with_num_members' is True
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count('member'))

        # Limit queryset by quantity if provided
        if qty:
            self.queryset = self.queryset[:int(qty)]
            print('queryset', self.queryset)

        # Filter queryset by server ID if provided
        if by_serverid:
            try:
                self.queryset = Server.objects.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server {by_serverid} does not exist.", code=400)
            except ValueError:
                raise ValidationError(
                    detail="Parameter error: server id must be a number.")

        # Serialize queryset and return response
        serializer = ServerSerializer(self.queryset, many=True, context={
                                      'with_num_members': with_num_members})
        return Response(serializer.data)
