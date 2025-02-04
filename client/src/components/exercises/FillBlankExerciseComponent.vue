<template>
    <div class="fill-blank-exercise">
      <div class="row justify-content-center">
        <div v-for="(item, itemIndex) in parsedData" :key="itemIndex" class="col-md-6 col-lg-4 mb-3">
          <div class="card bg-light p-2 text-center">
            <div 
                class="d-flex justify-content-center align-items-center position-relative"
                    v-tooltip="{
                        content: item.answersHint,
                        shown: isShowHints,
                        triggers: [],
                        delay: 0
                    }"
                >
                <span>{{ item.textBefore }}</span>
                <div class="position-relative d-flex align-items-center">
                  <input 
                    :ref="'inputField' + itemIndex"
                    v-model="userAnswers[itemIndex]" 
                    :style="{ width: `${item.placeholderLength * 0.5}em`, color: results[itemIndex] === undefined ? 'black' : results[itemIndex] ? 'green' : 'red' }" 
                    class="form-control mx-1 input-field" 
                    @input="checkAnswer(itemIndex)"
                    @focus="handleFocus(itemIndex)"
                  />
                </div>
                <span v-if="item.textAfter">{{ item.textAfter }}</span>
                <span v-if="results[itemIndex] !== undefined" class="position-absolute result-icon">
                  <font-awesome-icon 
                    :icon="results[itemIndex] ? ['fas', 'check'] : ['fas', 'xmark']" 
                    :class="results[itemIndex] ? 'text-success' : 'text-danger'" 
                  />
                </span>
            </div>
          </div>
        </div>
      </div>
      <div class="d-flex justify-content-between mt-3">
        <div class="btn-group">
            <SpecialCharsButtons
                :specialChars="specialChars"
                @diacrt-click="handleDiacrtButtonClick"            
              />
        </div>
        <button class="btn btn-light border-dark" 
                ref="hintButton" 
                @pointerdown="isShowHints = true"
                @pointerup="isShowHints = false"  
                @mouseleave="isShowHints = false">
          <font-awesome-icon :icon="['fas', 'key']" />
        </button>
      </div>
    </div>
  </template>
  
  
  <script>
  import SpecialCharsButtons from '@/components/ui/SpecialCharsButtons.vue';
  
  export default {
    name: 'FillBlankExercise',
    components: {
      SpecialCharsButtons,
    },
    props: {
      exercise: {
        type: Object,
        required: false,
      },
    },
    data() {
      return {
        userAnswers: [], 
        results: [], 
        parsedData: [],
        isShowHints: false,
        activeIndex: null,
      };
    },
    methods: {
      parseData() {
        this.parsedData = this.exercise.data.map(item => {
          /*
            This regular expression is used to extract different parts of a string from the question.
            - (.*) - captures any sequence of characters before the opening square bracket
            - [. \[\*\*+: - captures the opening square bracket [, followed by one or more asterisks (**) and a colon :.
            - (.*)\] - captures any sequence of characters between the colon and the closing square bracket ].
            - (.*)? - captures any sequence of characters after the closing square bracket (optional).
          */
          const match = item.question.match(/(.*)\[(\*\*+):(.*)\](.*)?/);
          if (match) {
            const correctAnswers = match[3].split('|');
            return {
              textBefore: match[1],
              placeholderLength: match[2].length,
              correctAnswers: correctAnswers,
              textAfter: match[4] || '',
              answersHint: correctAnswers.map(ans => `${match[1]}${ans}${match[4] || ''}`).join(', '),
            };
          }
          return {};
        });
      },
      checkAnswer(itemIndex) {
        if (this.userAnswers[itemIndex] === '') {
            this.results[itemIndex] = undefined;
            return;
        }
        const correctAnswers = this.parsedData[itemIndex].correctAnswers;
        const userAnswer = this.userAnswers[itemIndex].toLowerCase();
        const isCorrect = correctAnswers.includes(userAnswer);
        this.results[itemIndex] = isCorrect;
      },    
      handleFocus(itemIndex) {
        this.activeIndex = itemIndex;
      },
      handleDiacrtButtonClick(event) {
        if (this.activeIndex === null) {
          console.error("No active input field.");
          return;
        }
  
        const char = event.target.dataset.char;
        const activeElement = this.$refs[`inputField${this.activeIndex}`][0];
        
        if (activeElement) {
          const position = activeElement.selectionStart;
          const updatedText = [
            activeElement.value.slice(0, position),
            char,
            activeElement.value.slice(position)
          ].join('');
          this.userAnswers[this.activeIndex] = updatedText; // обновляем поле ввода
          this.$nextTick(() => {
            activeElement.focus();
            activeElement.selectionStart = activeElement.selectionEnd = position + 1;
            this.checkAnswer(this.activeIndex); // обновляем результат
          });
        }
      },
    },
    created() {
      this.parseData();
      this.userAnswers = this.parsedData.map(() => '');
      this.results = this.parsedData.map(() => undefined);
    },
  };
  </script>
  
  <style scoped>
  .fill-blank-exercise {
    font-size: 1.1em;
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
    font-size: 1.1em; 
    text-align: center;
  }
  
  .position-relative {
    position: relative;
  }
  
  .ms-2 {
    margin-left: 1rem;
  }
  
  .result-icon {
    top: 50%;
    transform: translateY(-50%);
    right: -1.5em;
  }
  
  .text-center {
    text-align: center;
  }
  </style>
  