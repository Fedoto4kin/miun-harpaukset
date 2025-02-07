<template>
    <div class="fill-blank-text-exercise">
    <div class="d-flex flex-row-reverse">
        <button 
          class="btn btn-outline-primary"
          @click="checkAnswers"
          title="Kuotele otviettua"
        >
        <font-awesome-icon :icon="['fas', 'spell-check']" />
        </button>
    </div>
      <div 
        v-for="(sentence, sentenceIndex) in parsedText" 
        :key="sentenceIndex" 
        class="pe-1 d-inline-flex flex-wrap pe-2 mb-2"
    >
        <div 
            v-for="(part, partIndex) in sentence" 
            :key="partIndex" 
            class="d-inline position-relative"           
        >
          <span v-if="part.type === 'text'">{{ part.value }}</span>
          <input
            v-else
            v-model="userAnswers[sentenceIndex][partIndex]"
            :ref="'inputField' + sentenceIndex + '-' + partIndex"
            :style="{ 
              width: `${part.placeholderLength * 0.6}em`, 
              color: results[sentenceIndex][partIndex] === undefined ? 'black' : results[sentenceIndex][partIndex] ? 'green' : 'red' 
            }"
            class="form-control mx-1 input-field"
            @input="handleInputChange"
            @focus="handleFocus(sentenceIndex, partIndex)"
            v-tooltip.right="{
                content: part.correctAnswer,
                shown: isShowHints,
                triggers: [],
                delay: 0,
              }"
          />
          <span v-if="results[sentenceIndex][partIndex] !== undefined" class="position-absolute result-icon">
            <font-awesome-icon 
              :icon="results[sentenceIndex][partIndex] ? ['fas', 'check'] : ['fas', 'xmark']" 
              :class="results[sentenceIndex][partIndex] ? 'text-success' : 'text-danger'" 
            />
          </span>
        </div>
      </div>
  
      <div class="d-flex justify-content-between mt-3">
        <div class="btn-group">
          <SpecialCharsButtons @diacrt-click="handleDiacrtButtonClick" />
        </div>
        <HintButton @show-hint="isShowHints = $event" />
      </div>
    </div>
  </template>
  
  <script>
  import SpecialCharsButtons from '@/components/ui/SpecialCharsButtons.vue';
  import HintButton from '@/components/ui/HintButtonCompponent.vue';
  
  export default {
    name: 'FillBlankTextExercise',
    components: {
      SpecialCharsButtons,
      HintButton,
    },
    props: {
      exercise: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        userAnswers: [],
        results: [],
        isShowHints: false,
        activeSentenceIndex: null,
        activePartIndex: null,
      };
    },
    computed: {
      parsedText() {
        if (!this.exercise.data.text) {
          return [];
        }
        const regex = /\[(\d+)\*:([^\]]+)\]/g;
  
        return this.exercise.data.text.map((sentence) => {
          const parts = [];
          let lastIndex = 0;
          let match;
  
          while ((match = regex.exec(sentence)) !== null) {
            if (match.index > lastIndex) {
              parts.push({
                type: 'text',
                value: sentence.slice(lastIndex, match.index),
              });
            }
  
            parts.push({
              type: 'blank',
              id: match[1], // Идентификатор пропуска
              placeholderLength: Number(match[1])+2, // Длина строки в квадратных скобках
              correctAnswer: match[2], // Правильный ответ
            });
  
            lastIndex = match.index + match[0].length;
          }
          if (lastIndex < sentence.length) {
            parts.push({
              type: 'text',
              value: sentence.slice(lastIndex),
            });
          }
  
          return parts;
        });
      },
    },
    methods: {
      parseData() {
        this.userAnswers = this.parsedText.map((sentence) => sentence.map(() => ''));
        this.results = this.parsedText.map((sentence) => sentence.map(() => undefined));
      },
      clearResult() {
        this.results = this.parsedText.map((sentence) => sentence.map(() => undefined));
      },
      checkAnswers() {
        this.parsedText.forEach((sentence, sentenceIndex) => {
          sentence.forEach((part, partIndex) => {
            if (part.type === 'blank') {
              const userAnswer = this.userAnswers[sentenceIndex][partIndex]?.toLowerCase();
              const isCorrect = part.correctAnswer === userAnswer;
              this.results[sentenceIndex][partIndex] = isCorrect;
            }
          });
        });
      },
      handleFocus(sentenceIndex, partIndex) {
        this.activeSentenceIndex = sentenceIndex;
        this.activePartIndex = partIndex;
      },
      handleInputChange() {
        this.clearResult();
      },
      handleDiacrtButtonClick(event) {
        this.clearResult();
        if (this.activeSentenceIndex === null || this.activePartIndex === null) {
          console.error('No active input field.');
          return;
        }
  
        const char = event.target.dataset.char;
        const activeElement = this.$refs[`inputField${this.activeSentenceIndex}-${this.activePartIndex}`][0];
  
        if (activeElement) {
          const position = activeElement.selectionStart;
          const updatedText = [
            activeElement.value.slice(0, position),
            char,
            activeElement.value.slice(position),
          ].join('');
          this.userAnswers[this.activeSentenceIndex][this.activePartIndex] = updatedText;
          this.$nextTick(() => {
            activeElement.focus();
            activeElement.selectionStart = activeElement.selectionEnd = position + 1;
          });
        }
      },
    },
    created() {
      this.parseData();
    },
  };
  </script>
  
  <style scoped>

  .fill-blank-text-exercise {
    font-size: 1.125em;
  }

  .input-field {
    display: inline-block;
    width: auto;
    min-width: 40px;
    border: none;
    border-bottom: 1px solid #ccc;
    outline: none;
    box-shadow: none;
    padding: 0 5px 0 0.3em;
    font-size: 1em;
    margin: 0 0.2em;
  }
  
  .result-icon {
    top: 50%;
    transform: translateY(-50%);
    right: 0.1em;
  }
  
  .text-center {
    text-align: center;
  }
  </style>
  