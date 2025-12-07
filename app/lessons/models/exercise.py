from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from enum import Enum


class ExerciseType(Enum):

    ''' 
        Interactive hint exercise - shows text with clickable hints
    '''
    INTERACTIVE_HINT = ("InteractiveHint", "Interactive Hints")
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
        A sentence assembly exercise with pre-filled slots where users
        construct a sentence by arranging given words in the correct order,
        while some slots are pre-filled.
    '''
    SENTENCE_ASSEMBLY_WITH_PREFILL = ("SentenceAssemblyPrefilled", "Sentence Assembly with Prefill")
    
    ''' 
        A match-the-pair exercise where users find the 
        corresponding pair for a given word.
    '''
    MATCH_PAIR = ("MatchPair", "Match the Pair")

    ''' 
        A match-the-pair exercise where pair/word can have multiple 
        correct answers and selected options don't disappear.
    '''
    MATCH_PAIR_MULTIPLE = ("MatchPairMultiple", "Match the Pair (Multiple)")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label
    
    ''' 
        A fill-in-the-blank exercise where users fill 
        in missing words in a given table.
    '''
    FILL_BLANK_TABLE = ("FillBlankTable", "Fill in the Blank Table")

    ''' 
        A match-the-pair exercise where users find the 
        corresponding pair for a given word.
    '''
    MATCH_PAIR_SLOTS = ("MatchPairSentenceSlot", "Match the Pair with slots for sentantions")

    ''' 
        A fill-in-the-blank exercise where users fill 
        in missing parts of a text by selecting the correct
        answer from provided options.
    '''
    FILL_GAP_WITH_CHOICE = ("FillGapWithChoice", "Fill Gap with Choice")

    '''
        A word search exercise where users find 
        and select words hidden in a grid of letters.
    '''
    FILL_WORD = ("FillWord", "Fillword Game")


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
    has_answers_check = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Annanda'
        verbose_name_plural = 'Annandat'

    def __str__(self):
        return f"{self.get_exercise_type_display()}: {self.module}"
