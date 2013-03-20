from rest_framework import serializers
from .models import Passage


class PassageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passage
        exclude = ('id', 'source',)


class DefinitionSerializer(serializers.Serializer):
    text = serializers.CharField()
    lexical_type = serializers.CharField()
    lemmas = serializers.CharField()
