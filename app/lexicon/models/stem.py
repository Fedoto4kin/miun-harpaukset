# app/lexicon/models/stem.py
from django.db import models
from .word import Word


class Stem(models.Model):
    """
    Основа слова для словообразования.
    
    НУМЕРАЦИЯ (храним ВСЕ основы как ПОЛНЫЕ формы):
    - Глаголы: 9 основ (0-8)
    - Существительные: 6 основ (0-5)
    - Прилагательные: 6 основ (0-5)
    
    Правила импорта:
    1. Основа 0 = начальная форма (лемма)
    2. Остальные основы = база + суффикс из шаблона
    3. Если чередование указано (через :), сохраняем обе полные формы
    4. Если чередования нет, для сильных основ (2 и 5) 
       сохраняем ТУ ЖЕ полную форму, что и для слабых (1 и 4)
    """
    
    # ГЛАГОЛЫ - 8 основ (0-7)
    class VerbStemType(models.TextChoices):
        VERB_0 = 'verb_0', 'Основа 0 (начальная форма - инфинитив)'
        VERB_1 = 'verb_1', 'Основа 1 (слабая презенс)'
        VERB_2 = 'verb_2', 'Основа 2 (сильная презенс)'
        VERB_3 = 'verb_3', 'Основа 3 (слабая имперфект)'
        VERB_4 = 'verb_4', 'Основа 4 (сильная имперфект)'
        VERB_5 = 'verb_5', 'Основа 5 (сильная/согласная)'
        VERB_6 = 'verb_6', 'Основа 6 (пассив слабая)'
        VERB_7 = 'verb_7', 'Основа 7 (пассив сильная)'
    
    # СУЩЕСТВИТЕЛЬНЫЕ - 6 основ (0-5)
    class NounStemType(models.TextChoices):
        NOUN_0 = 'noun_0', 'Основа 0 (начальная форма - номинатив ед.ч.)'
        NOUN_1 = 'noun_1', 'Основа 1 (слабая ед.ч.)'
        NOUN_2 = 'noun_2', 'Основа 2 (сильная ед.ч.)'
        NOUN_3 = 'noun_3', 'Основа 3 (партитив ед.ч.)'
        NOUN_4 = 'noun_4', 'Основа 4 (слабая мн.ч.)'
        NOUN_5 = 'noun_5', 'Основа 5 (сильная мн.ч.)'
    
    # ПРИЛАГАТЕЛЬНЫЕ - 6 основ (0-5)
    class AdjStemType(models.TextChoices):
        ADJ_0 = 'adj_0', 'Основа 0 (начальная форма - номинатив ед.ч.)'
        ADJ_1 = 'adj_1', 'Основа 1 (слабая ед.ч.)'
        ADJ_2 = 'adj_2', 'Основа 2 (сильная ед.ч.)'
        ADJ_3 = 'adj_3', 'Основа 3 (партитив ед.ч.)'
        ADJ_4 = 'adj_4', 'Основа 4 (слабая мн.ч.)'
        ADJ_5 = 'adj_5', 'Основа 5 (сильная мн.ч.)'
    
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name='stems'
    )
    
    stem_type = models.CharField(
        max_length=20,
        choices=VerbStemType.choices + NounStemType.choices + AdjStemType.choices
    )
    
    # Номер основы (0-8 для глаголов, 0-5 для именных)
    number = models.PositiveSmallIntegerField()
    
    # ПОЛНЫЙ текст основы (база + суффикс)
    form = models.CharField(
        max_length=256
    )
    
    # Специальные пометы
    SPECIAL_MARKS = [
        ('', 'Нет пометы'),
        ('pl', 'Только мн.ч. (pl.)'),
        ('sing', 'Только ед.ч. (sing.)'),
        ('v_def', 'Только 3 л. (v. def.)'),
    ]
    special_mark = models.CharField(
        max_length=10,
        choices=SPECIAL_MARKS,
        blank=True,
        default=''
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Vardalo'
        verbose_name_plural = 'Vardalot'
        unique_together = ['word', 'stem_type']
        ordering = ['word', 'number']
        indexes = [
            models.Index(fields=['word', 'number']),
            models.Index(fields=['word']),
        ]
    
    def __str__(self):
        mark = f" [{self.special_mark}]" if self.special_mark else ""
        return f"{self.word.word_clean} - {self.number}: {self.form} {mark}"
    
    @property
    def is_verb(self):
        return self.stem_type.startswith('verb_')
    
    @property
    def is_noun(self):
        return self.stem_type.startswith('noun_')
    
    @property
    def is_adj(self):
        return self.stem_type.startswith('adj_')
    
    
    @classmethod
    def get_stem_type_for_number(cls, pos_abbr, number):
        """
        Возвращает тип основы по номеру и части речи.
        """
        if pos_abbr == 'v.':
            return getattr(cls.VerbStemType, f'VERB_{number}', None)
        elif pos_abbr == 's.':
            return getattr(cls.NounStemType, f'NOUN_{number}', None)
        elif pos_abbr == 'a.':
            return getattr(cls.AdjStemType, f'ADJ_{number}', None)
        return None
    
    @classmethod
    def create_stem(cls, word, number, form, special_mark=''):
        """
        Создает основу с заданным номером.
        """
        stem_type = cls.get_stem_type_for_number(word.pos.abbr, number)
        if not stem_type:
            return None
        
        return cls.objects.create(
            word=word,
            stem_type=stem_type,
            number=number,
            form=form,
            special_mark=special_mark
        )
    
    @classmethod
    def get_stem_by_number(cls, word, number):
        """
        Возвращает основу по слову и номеру.
        """
        return cls.objects.filter(word=word, number=number).first()
    
    @classmethod
    def get_all_stems_for_word(cls, word):
        """
        Возвращает все основы слова в виде словаря {номер: форма}.
        """
        stems = cls.objects.filter(word=word).order_by('number')
        return {stem.number: stem.form for stem in stems}
