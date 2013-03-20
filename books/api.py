from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from tastypie.resources import ModelResource
from tastypie import fields
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Author, Book, Passage
from .serializers import PassageSerializer, DefinitionSerializer
import dictionary


class PassageListApi(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        passages = Passage.objects.all()
        serializer = PassageSerializer(passages)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PassageSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PassageApiDetail(APIView):
    """
    Retrieve, update or delete a passage instance.
    """
    def get_object(self, pk):
        try:
            return Passage.objects.get(pk=pk)
        except Passage.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        passage = self.get_object(pk)
        serializer = PassageSerializer(passage)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        passage = self.get_object(pk)
        serializer = PassageSerializer(passage, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        passage = self.get_object(pk)
        passage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#class DictionaryListApi(JSONResponseMixin, SingleObjectMixin, View):
class DictionaryListApi(APIView):
    """
    List all snippets, or create a new snippet.
    """

    #model = Dictionary

    def get(self, request, word, format=None):
        definitions = dictionary.lookup(word)
        serializer = DefinitionSerializer(definitions[:5])
        return Response({'definitions': serializer.data})

