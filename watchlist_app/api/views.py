# from django.shortcuts import render
from watchlist_app import models
from watchlist_app.api import serializers, permissions, pagination
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
# from rest_framework import mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from user_app.api import throttling
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class UserReview(generics.ListAPIView):
    # throttle_classes = [throttling.ReviewListThrottle, AnonRateThrottle]
    # queryset = models.Review.objects.all()
    serializer_class = serializers.reviewserielizer
    # permission_classes = [IsAuthenticated]
    
    # def get_queryset(self):
    #     username = self.kwargs['username']                                                  #Here we are simply passing http://127.0.0.1:8000/watch/review/ankur/ to get the details
    #     return models.Review.objects.filter(review_user__username=username)                 #__username used to specify the foreign key will be username. Filtering against the URL
    
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return models.Review.objects.filter(review_user__username=username)                   #Here we are simply passing http://127.0.0.1:8000/watch/review/?username=ankur
                                                                                              #Filtering against the query parameters
class Reviewlist(generics.ListAPIView):
    # throttle_classes = [throttling.ReviewListThrottle, AnonRateThrottle]
    # queryset = models.Review.objects.all()
    serializer_class = serializers.reviewserielizer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Review.objects.filter(watchli=pk)
    
class ReviewCreate(generics.CreateAPIView):
    # throttle_classes = [throttling.ReviewCreateThrottle]
    def get_queryset(self):                                   
        return models.Review.objects.all()
    
    serializer_class = serializers.reviewserielizer
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')                                                                                              # perform_create(self, serializer) - Called by CreateModelMixin when saving a new object instance.
        movie = models.watchlist.objects.get(pk=pk)                                                                                              # perform_update(self, serializer) - Called by UpdateModelMixin when saving an existing object instance.
        review_user = self.request.user                                                               #Here we are fetching all the user who have written some review
        review_queryset = models.Review.objects.filter(watchli=movie, review_user=review_user)           #Here we are filtering according to the movie and review user
        
        if review_queryset.exists():                                                                #If that user's review exists already then we are raiseing an exception if not then we are saving the review
            raise ValidationError('You have already reviewed this movie')                                                                                              # perform_destroy(self, instance) - Called by DestroyModelMixin when deleting an object instance.
    
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2
        movie.number_rating = movie.number_rating + 1
        movie.save()  
        serializer.save(watchli=movie, review_user=review_user)
        
                
class Reviewdetails(generics.RetrieveUpdateDestroyAPIView):                                           #It can retrieve, update and delete a review. Functionalities are inbuilt.
    queryset = models.Review.objects.all()
    serializer_class = serializers.reviewserielizer
    permission_classes = [permissions.ReviewUserOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

# class Reviewdetails(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = models.Review.objects.all()
#     serializer_class = serializers.reviewserielizer
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class Reviewlist(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = models.Review.objects.all()
#     serializer_class = serializers.reviewserielizer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class streamplatformsVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = models.streamplatform.objects.all()
#         serializer = serializers.streamplatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = models.streamplatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = serializers.streamplatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = serializers.streamplatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors) 

class streamplatformsVS(viewsets.ModelViewSet):
    queryset = models.streamplatform.objects.all()
    serializer_class = serializers.streamplatformSerializer
    permission_classes = [permissions.AdminOrReadOnly]

class streamplatformAV(APIView):
    permission_classes = [permissions.AdminOrReadOnly]
    def get(self, request):
        platform = models.streamplatform.objects.all()
        serializer = serializers.streamplatformSerializer(platform, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.streamplatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors) 
    
class StreamPlatformdetail(APIView):
    permission_classes = [permissions.AdminOrReadOnly]
    def get(self, request, pk):
        try:
            platform = models.streamplatform.objects.get(pk=pk)
        except models.streamplatform.DoesNotExist:
            return Response({'Error': 'Stream platform does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.streamplatformSerializer(platform)
        return Response(serializer.data)
            
    def put(self, request, pk):
        platform = models.streamplatform.objects.get(pk=pk)
        serializer = serializers.streamplatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        platform = models.streamplatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WatchlistGV(generics.ListAPIView):
    # throttle_classes = [throttling.ReviewListThrottle, AnonRateThrottle]
    queryset = models.watchlist.objects.all()
    serializer_class = serializers.watchlistSerializer
    pagination_class = pagination.CurserPagination
    # permission_classes = [IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]                              #http://127.0.0.1:8000/watch/list2/?title=Harry Potter
    # filterset_fields = ['title', 'platform__name']                       #We can filter by title and platform by giving exact name of the title and platform
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name']                            #http://127.0.0.1:8000/watch/list2/?search=Hu
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']

class watchlistAV(APIView):
    permission_classes = [permissions.AdminOrReadOnly]
    def get(self, request):
        movie = models.watchlist.objects.all()
        serializer = serializers.watchlistSerializer(movie, many=True)                
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.watchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class WatchDetailAV(APIView):
    permission_classes = [permissions.AdminOrReadOnly]
    def get(self, request, pk):
        try:
            movie = models.watchlist.objects.get(pk=pk)                                       
        except models.watchlist.DoesNotExist:
            return Response({'Error': "Movie Not Found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = serializers.watchlistSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = models.watchlist.objects.get(pk=pk)
        serializer = serializers.watchlistSerializer(movie, data=request.data) 
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        movie = models.watchlist.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Function based views
# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movie = Movie.objects.all()
#         serializer = serializers.MovieSerializer(movie, many=True)                #Since we are fetching all data from Movie we need to tell serializer that all data has to be taken into account
#         return Response(serializer.data)                                          #.data will take all the data from serializer
    
#     elif request.method == 'POST':
#         serializer = serializers.MovieSerializer(data=request.data)               #Entered data will be saved in serializer
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.error)
        
        
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET':
        
#         try:
#             movie = Movie.objects.get(pk=pk)                                       #Here only pk (one) entity is there so we are not using many
#         except Movie.DoesNotExist:
#             return Response({'Error': "Movie Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = serializers.MovieSerializer(movie)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = serializers.MovieSerializer(movie, data=request.data) 
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        