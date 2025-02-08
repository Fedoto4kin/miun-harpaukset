from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from enum import Enum


class ExerciseType(Enum):

    ''' 
        A fill-in-the-blank exercise where users 
        complete words by filling in missing parts.
    '''
    FILL_BLANK = ("FillBlank", "Fill in the Blank Words")
    
    ''' 
        A syllable assembly exercise where users construct a word
        by arranging given syllables in the correct order.
    '''
    SYLLABLE_ASSEMBLY = ("SyllableAssembly", "Syllable Assembly")
    
    ''' 
        A fill-in-the-blank exercise where users fill 
        in missing words in a given text.
    '''
    FILL_BLANK_TEXT = ("FillBlankText", "Fill in the Blank Text")

    ''' 
        A sentence assembly exercise where users construct a sentence
        by arranging given words in the correct order.
    '''
    SENTENCE_ASSEMBLY = ("SentenceAssembly", "Sentence Assembly")
    
    ''' 
        A match-the-pair exercise where users find the 
        corresponding pair for a given word.
    '''
    MATCH_PAIR = ("MatchPair", "Match the Pair")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def choices(cls):
        return [(tag.value, tag.label) for tag in cls]


class Exercise(models.Model):
    module = models.ForeignKey(
        'Module',
        on_delete=models.CASCADE,
        related_name='exercises'
    )
    exercise_type = models.CharField(
        max_length=50,
        choices=ExerciseType.choices(),
    )
    data = models.JSONField(
        encoder=DjangoJSONEncoder,
        default=dict,
        blank=True
    )

    class Meta:
        verbose_name = 'Annanda'
        verbose_name_plural = 'Annandat'

    def __str__(self):
        return f"{self.get_exercise_type_display()}: {self.module}"
