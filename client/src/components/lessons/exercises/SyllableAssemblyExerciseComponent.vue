<template>
    <div class="syllable-assembly-exercise mt-1">
      <div class="row justify-content-center">
        <div
          v-for="(question, questionIndex) in parsedQuestions"
          :key="questionIndex"
          class="w-auto mb-2 px-3"
        >
          <div class="card bg-light px-3 w-auto d-flex">
            <div class="d-flex justify-content-center align-items-center position-relative">
              <!-- Отображение слогов -->
              <div class="syllables-container">
                <span
                  v-for="(syllable, syllableIndex) in question.syllables"
                  :key="syllableIndex"
                  class="btn btn-outline-secondary syllable"
                  @click="selectSyllable(questionIndex, syllableIndex)"
                >
                  {{ syllable }}
                </span>
              </div>
  
              <!-- Поле для сборки слова и кнопка очистки -->
              <div
                class="mt-3 d-flex align-items-center"
                v-tooltip="{
                  content: question.word,
                  shown: isShowHints,
                  triggers: [],
                  delay: 0,
                }"
              >
                <div class="input-group">
                  <input
                    v-model="userAnswers[questionIndex]"
                    :style="{ 
                        width: `${question.word.length * 0.65}em`, 
                        color: results[questionIndex] === undefined ? 'black' : results[questionIndex] ? 'green' : 'red' 
                    }"
                    class="form-control mx-1 input-field"
                    @input="checkAnswer(questionIndex)"
                  />
                  <div class="input-group-append">
                    <button
                      :class="{
                        'btn btn-link btn-clear btn-sm': true,
                        'text-black': userAnswers[questionIndex],
                        'text-secondary': !userAnswers[questionIndex],
                      }"
                      :disabled="!userAnswers[questionIndex]"
                      @click="clearField(questionIndex)"
                    >
                      <font-awesome-icon :icon="['fas', 'delete-left']" />
                    </button>
                  </div>
                </div>
              </div>
  
              <!-- Иконка результата -->
              <span
                v-if="results[questionIndex] !== undefined"
                class="position-absolute result-icon"
              >
                <font-awesome-icon
                  :icon="results[questionIndex] ? ['fas', 'check'] : ['fas', 'xmark']"
                  :class="results[questionIndex] ? 'text-success' : 'text-danger'"
                />
              </span>
            </div>
          </div>
        </div>
      </div>
      <div class="d-flex justify-content-end">
          <HintButton @show-hint="isShowHints = $event" />
      </div>
    </div>
  </template>
  
<script>

  import HintButton from '@/components/ui/HintButtonCompponent.vue';

  export default {
    name: 'SyllableAssemblyExercise',
    components: {
      HintButton,
    },
    props: {
      data: {
        type: Object,
        required: true,
      },
      hasCheck: {
        type: Boolean,
        required: false,
        default: true,
      },
    },
    data() {
      return {
        userAnswers: [], // Ответы пользователя
        results: [], // Результаты проверки
        parsedQuestions: [], // Парсированные вопросы
        isShowHints: false, // Показывать ли подсказки
        activeQuestionIndex: null, // Активный вопрос
      };
    },
    methods: {
      // Парсинг данных задания
      parseData() {
        this.parsedQuestions = this.data.questions.map((question) => ({
          syllables: question.syllables,
          word: question.word,
        }));
      },
      // Проверка ответа
      checkAnswer(questionIndex) {
        const userAnswer = this.userAnswers[questionIndex];
        const correctAnswer = this.parsedQuestions[questionIndex].word;
  
        // Проверка только если введено >= символов, чем в правильном ответе
        if (userAnswer.length >= correctAnswer.length) {
          const isCorrect = userAnswer.toLowerCase() === correctAnswer.toLowerCase();
          this.results[questionIndex] = isCorrect;
        } else {
          this.results[questionIndex] = undefined; // Сброс результата, если символов недостаточно
        }
      },
      // Выбор слога
      selectSyllable(questionIndex, syllableIndex) {
        const syllable = this.parsedQuestions[questionIndex].syllables[syllableIndex];
        this.userAnswers[questionIndex] += syllable;
        this.checkAnswer(questionIndex);
      },
      // Очистка поля
      clearField(questionIndex) {
        this.userAnswers[questionIndex] = '';
        this.results[questionIndex] = undefined; // Сброс результата
      },
      // Фокус на поле ввода
      handleFocus(questionIndex) {
        this.activeQuestionIndex = questionIndex;
      },
      // Обработка нажатия на кнопку с диакритическими знаками
      handleDiacrtButtonClick(event) {
        if (this.activeQuestionIndex === null) {
          console.error('No active input field.');
          return;
        }
  
        const char = event.target.dataset.char;
        const activeElement = this.$refs[`inputField${this.activeQuestionIndex}`][0];
  
        if (activeElement) {
          const position = activeElement.selectionStart;
          const updatedText = [
            activeElement.value.slice(0, position),
            char,
            activeElement.value.slice(position),
          ].join('');
          this.userAnswers[this.activeQuestionIndex] = updatedText;
          this.$nextTick(() => {
            activeElement.focus();
            activeElement.selectionStart = activeElement.selectionEnd = position + 1;
            this.checkAnswer(this.activeQuestionIndex);
          });
        }
      },
    },
    created() {
      this.parseData();
      this.userAnswers = this.parsedQuestions.map(() => '');
      this.results = this.parsedQuestions.map(() => undefined);
    },
  };
  </script>
  
  <style scoped>
  
  .syllable-assembly-exercise {
    font-size: 1em;
  }
  
  .syllables-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.7rem;
    justify-content: center;
  }
  
  .input-field {
    display: inline-block;
    width: auto;
    min-width: 40px;
    border: none;
    border-bottom: 1px solid #ccc;
    outline: none;
    box-shadow: none;
    padding: 0 5px;
    font-size: 1.35em;
    text-align: center;
    margin-bottom: 0.5em;
    margin-left: 1rem !important;
  }
  
  .result-icon {
    top: 50%;
    transform: translateY(-50%);
    right: -1.9em;
  }
  
 .btn-clear {
    padding: 0 0.2em;
    margin-top: 0.5em;
  }

  .btn-link {
    text-decoration: none;
  }
  
  .btn-link:disabled {
    cursor: not-allowed;
    opacity: 0.6;
  }
  </style>