from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie
from .serializers import MovieSerializer

# GET (all) + POST
@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# here we have to except get and post method because this view is for single object
# GET (single) + PUT + PATCH + DELETE
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def movie_detail(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == 'DELETE':
        movie.delete()
        return Response({'msg': 'Movie deleted successfully'})

# added more functions
# added more urls