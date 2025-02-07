<template>
  <div class="fill-blank-text-exercise">
    <div v-if="parsedExample.length" class="example-section">
      <h4>Пример:</h4>
      <div class="example-text">
        <div v-for="(part, partIndex) in parsedExample" :key="partIndex" class="d-inline position-relative">
          <span v-if="part.type === 'text'">{{ part.value }}</span>
          <span v-else class="example-blank">{{ part.correctAnswer }}</span>
        </div>
      </div>
    </div>

    <div v-for="(textObj, textIndex) in parsedTexts" :key="textIndex" class="text-section">
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
        v-for="(sentence, sentenceIndex) in textObj.text" 
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
            v-model="userAnswers[textIndex][sentenceIndex][partIndex]"
            :ref="'inputField' + textIndex + '-' + sentenceIndex + '-' + partIndex"
            :style="{ 
                width: `${part.placeholderLength * 0.6}em`, 
                color: results[textIndex][sentenceIndex][partIndex] === undefined ? 'black' : results[textIndex][sentenceIndex][partIndex] ? 'green' : 'red' 
            }"
            class="form-control mx-1 input-field"
            @input="handleInputChange"
            @focus="handleFocus(textIndex, sentenceIndex, partIndex)"
            v-tooltip.right="{
                content: part.correctAnswer,
                shown: isShowHints,
                triggers: [],
                delay: 0,
            }"
          />
          <span v-if="results[textIndex][sentenceIndex][partIndex] !== undefined" class="position-absolute result-icon">
            <font-awesome-icon 
              :icon="results[textIndex][sentenceIndex][partIndex] ? ['fas', 'check'] : ['fas', 'xmark']" 
              :class="results[textIndex][sentenceIndex][partIndex] ? 'text-success' : 'text-danger'" 
            />
          </span>
        </div>
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
      activeTextIndex: null,
      activeSentenceIndex: null,
      activePartIndex: null,
    };
  },
  computed: {
    // Парсинг примера
    parsedExample() {
      return this.exercise.data.example ? this.parseText([this.exercise.data.example]) : [];
    },
    // Парсинг текстов
    parsedTexts() {
      if (!this.exercise.data.texts) {
        return [];
      }
      return this.exercise.data.texts.map((textObj) => ({
        hint: textObj.hint,
        text: this.parseText(textObj.text),
      }));
    },
  },
  methods: {
    parseText(textArray) {
      const regex = /\[(\d+)\*:([^\]{]+)({[^}]+})?\]/g;
      return textArray.map((sentence) => {
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
          const prefilledValue = match[3] ? match[3].slice(1, -1) : '';
          parts.push({
            type: 'blank',
            id: match[1],
            placeholderLength: Number(match[1]) + 2,
            correctAnswer: match[2],
            prefilledValue: prefilledValue,
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
    parseData() {
      this.userAnswers = this.parsedTexts.map((textObj) => 
        textObj.text.map((sentence) => 
          sentence.map((part) => (part.type === 'blank' ? part.prefilledValue : ''))
        )
      );
      this.results = this.parsedTexts.map((textObj) => 
        textObj.text.map((sentence) => 
          sentence.map(() => undefined)
        )
      );
    },
    clearResult() {
      this.results = this.parsedTexts.map((textObj) => 
        textObj.text.map((sentence) => 
          sentence.map(() => undefined)
        )
      );
    },
    checkAnswers() {
      this.parsedTexts.forEach((textObj, textIndex) => {
        textObj.text.forEach((sentence, sentenceIndex) => {
          sentence.forEach((part, partIndex) => {
            if (part.type === 'blank') {
              const userAnswer = this.userAnswers[textIndex][sentenceIndex][partIndex]?.toLowerCase();
              const isCorrect = part.correctAnswer === userAnswer;
              this.results[textIndex][sentenceIndex][partIndex] = isCorrect;
            }
          });
        });
      });
    },
    handleFocus(textIndex, sentenceIndex, partIndex) {
      this.activeTextIndex = textIndex;
      this.activeSentenceIndex = sentenceIndex;
      this.activePartIndex = partIndex;
    },
    handleInputChange() {
      this.clearResult();
    },
    handleDiacrtButtonClick(event) {
      this.clearResult();
      if (this.activeTextIndex === null || this.activeSentenceIndex === null || this.activePartIndex === null) {
        console.error('No active input field.');
        return;
      }
      const char = event.target.dataset.char;
      const activeElement = this.$refs[`inputField${this.activeTextIndex}-${this.activeSentenceIndex}-${this.activePartIndex}`][0];
      if (activeElement) {
        const position = activeElement.selectionStart;
        const updatedText = [
          activeElement.value.slice(0, position),
          char,
          activeElement.value.slice(position),
        ].join('');
        this.userAnswers[this.activeTextIndex][this.activeSentenceIndex][this.activePartIndex] = updatedText;
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
