from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from lexicon.models import Word, Definition, Pos, Base


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Base
        fields = ['id', 'base',]


class WordAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'word',]


class DefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definition
        fields = ['lang', 'definition']


class WordPreviewSerializer(serializers.ModelSerializer):

    definition = DefinitionSerializer(many=True, source='definition_set') 
    pos = serializers.CharField(source='pos.abbr', read_only=True)
    pos_name_ru = serializers.CharField(source='pos.name_ru', read_only=True)
    pos_name_fi = serializers.CharField(source='pos.name_fi', read_only=True)
    speech = serializers.FileField(source='speech.media', read_only=True)
    alias_words = WordAliasSerializer(many=True, source='alias')

    class Meta:
        model = Word
        fields = [
            'id',
            'word',
            'pos',
            'pos_name_ru',
            'pos_name_fi',
            'definition',
            'speech',
            'alias_words'
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
