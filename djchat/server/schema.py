from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializer import ServerSerializer, ChannelSerializer

server_list_docs = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="category",
            required=False,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Category of server to retrieve'),
        OpenApiParameter(
            name="qty",
            required=False,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Limit the number of servers returned."
        ),
        OpenApiParameter(
            name="by_user",
            required=False,
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Filter servers by user membership."
        ),
        OpenApiParameter(
            name="by_serverid",
            required=False,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Filter servers by server ID."
        ),
        OpenApiParameter(
            name="with_num_members",
            required=False,
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Include the number of members in the response."
        ),
    ]

)
