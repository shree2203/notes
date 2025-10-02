import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import UserSerializer

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        logger.info(f"Login request data: {request.data}")
        email = request.data.get('email')
        
        if not email:
            logger.error("No email provided in login request")
            return Response(
                {'error': 'Email is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            logger.info(f"Looking up user with email: {email}")
            user, created = User.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )
            
            if created:
                logger.info(f"Created new user with email: {email}")
                user.set_unusable_password()
                user.save()
            
            logger.info(f"Generating tokens for user: {email}")
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
            logger.info(f"Login successful for user: {email}")
            
            return Response(response_data)
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An error occurred during login'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
