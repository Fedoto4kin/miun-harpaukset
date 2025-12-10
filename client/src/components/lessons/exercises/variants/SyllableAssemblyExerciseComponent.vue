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
              <div class="my-2 d-flex align-items-center">
                <div class="d-inline-flex align-items-center position-relative input-wrapper">
                  <div class="position-relative">
                    <input
                      v-model="userAnswers[questionIndex]"
                      :ref="'inputField' + questionIndex"
                      :style="{ 
                          width: `${question.word.length * 0.7}em`, 
                          color: results[questionIndex] === undefined ? 'black' : results[questionIndex] ? 'green' : 'red' 
                      }"
                      class="form-control input-field"
                      @input="checkAnswer(questionIndex)"
                      @focus="handleFocus(questionIndex)"
                    />
                    
                    <!-- Подсказка поверх поля ввода -->
                    <div v-if="isShowHints && hintForField[questionIndex]"
                      class="hint-overlay"
                      :style="{ width: `${question.word.length * 0.7}em` }">
                      {{ question.word }}
                    </div>
                  </div>
                  
                  <button
                    :class="{
                      'btn btn-link btn-clear btn-sm ms-1': true,
                      'text-black': userAnswers[questionIndex],
                      'text-secondary': !userAnswers[questionIndex],
                    }"
                    :disabled="!userAnswers[questionIndex]"
                    @click="clearField(questionIndex)"
                    style="z-index: 3; position: relative; margin-top: 0;"
                  >
                    <font-awesome-icon :icon="['fas', 'delete-left']" />
                  </button>
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
        <HintButton @show-hint="toggleShowHints" />
      </div>
    </div>
  </template>
  
<script>
  import HintButton from '@/components/ui/HintButtonComponent.vue';
  import { confettiMixin } from '@/mixins/confettiMixin.js';

  export default {
    name: 'SyllableAssemblyExercise',
    mixins: [confettiMixin],
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
        userAnswers: [],
        results: [], 
        parsedQuestions: [], 
        isShowHints: false,
        activeQuestionIndex: null,
        hintForField: []
      };
    },
    methods: {
      parseData() {
        this.parsedQuestions = this.data.questions.map((question) => ({
          syllables: question.syllables,
          word: question.word,
        }));
      },
      checkAnswer(questionIndex) {
        const userAnswer = this.userAnswers[questionIndex];
        const correctAnswer = this.parsedQuestions[questionIndex].word;
  
        if (userAnswer.length >= correctAnswer.length) {
          const isCorrect = userAnswer.toLowerCase() === correctAnswer.toLowerCase();
          this.results[questionIndex] = isCorrect;
        } else {
          this.results[questionIndex] = undefined;
        }

        const allCorrect = this.results.flat().every(result => result === true);
        if (allCorrect) {
          this.launchConfetti();
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
        this.results[questionIndex] = undefined;
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
      
      toggleShowHints(show) {
        this.isShowHints = show;
        
        if (show) {
          this.hintForField = this.parsedQuestions.map(() => true);
        } else {
          this.hintForField = this.parsedQuestions.map(() => false);
        }
      }
    },
    created() {
      this.parseData();
      this.userAnswers = this.parsedQuestions.map(() => '');
      this.results = this.parsedQuestions.map(() => undefined);
      this.hintForField = this.parsedQuestions.map(() => false);
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
    padding: 4px;
    font-size: 1.35em;
    text-align: center;
    position: relative;
    z-index: 1;
    height: 1.8em;
    vertical-align: middle;
  }
  
  .result-icon {
    top: 50%;
    transform: translateY(-50%);
    right: -1em;
    z-index: 4;
  }
  
  .btn-clear {
    padding: 0.25rem 0.5rem;
    height: 42px; /* Такая же высота как у input */
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .btn-link {
    text-decoration: none;
  }
  
  .btn-link:disabled {
    cursor: not-allowed;
    opacity: 0.6;
  }
  
  .input-wrapper {
    display: inline-flex;
    align-items: center;
    margin-left: 1rem;
  }
  
  .position-relative {
    position: relative !important;
  }
  
  .hint-overlay {
    font-size: 1.35em;
    height: 38px;
    line-height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  
  </style>