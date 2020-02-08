from rest_framework import serializers
from lexicon.models import Word, Definition, Pos, Base

class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Base
        fields = ['id', 'base',]


class DefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definition
        fields = ['lang','definition']

class WordPreviewSerializer(serializers.ModelSerializer):

    definition = DefinitionSerializer(many=True, source='definition_set') 
    pos = serializers.CharField(source='pos.abbr', read_only=True)
    speech = serializers.FileField(source='speech.mp3', read_only=True  )

    class Meta:
        model = Word
        fields = [
            'id',
            'word',
            'pos',
            'definition',
            'speech'
        ]

class WordDetailSerializer(serializers.ModelSerializer):
    
    definition = DefinitionSerializer(many=True, source='definition_set') 
    pos = serializers.CharField(source='pos.abbr', read_only=True)


    class Meta:
        model = Word
        fields = [
            'id',
            'word',
            'pos',
            'definition',
        ]

class PosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pos
        fields = [
            'id',
            'abbr',
            'name_ru',
            'name_fi'
        ]        