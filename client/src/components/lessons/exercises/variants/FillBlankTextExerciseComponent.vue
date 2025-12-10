<template>
  <div class="fill-blank-text-exercise">
    <div v-if="parsedExample.length" class="example-section">
      <div class="example-text">
        <div v-for="(sentence, sentenceIndex) in parsedExample" :key="sentenceIndex"
          class="sentence d-inline-flex flex-wrap pe-2 mb-2">
          <div v-for="(part, partIndex) in sentence" :key="partIndex" class="d-inline position-relative">
            <span v-if="part.type === 'text'">{{ part.value }}</span>
            <span v-else :value="part.correctAnswers.join('|')" :style="{ width: `${part.placeholderLength * 0.6}em` }"
              class="form-control mx-1 input-field" disabled>{{ part.correctAnswers.join('|') }}</span>
          </div>
        </div>
      </div>
    </div>
    <div v-for="(textObj, textIndex) in parsedTexts" :key="textIndex" class="text-section">
      <div v-for="(sentence, sentenceIndex) in textObj.text" :key="sentenceIndex"
        class="d-inline-flex flex-wrap pe-2 mb-2">
        <div v-for="(part, partIndex) in sentence" :key="partIndex" class="d-inline position-relative input-wrapper">
          <span v-if="part.type === 'text'">{{ part.value }}</span>
          <input v-else v-model="userAnswers[textIndex][sentenceIndex][partIndex]"
            :ref="'inputField' + textIndex + '-' + sentenceIndex + '-' + partIndex" :style="{
              width: `${part.placeholderLength * 0.6}em`,
              color: results[textIndex][sentenceIndex][partIndex] === undefined ? 'black' : results[textIndex][sentenceIndex][partIndex] ? 'green' : 'red'
            }" class="form-control mx-1 input-field" @input="handleInputChange"
            @focus="handleFocus(textIndex, sentenceIndex, partIndex)"
            @blur="handleBlur(textIndex, sentenceIndex, partIndex)" />

          <!-- Подсказка поверх поля ввода -->
          <div v-if="isShowHints && hintForField[textIndex]?.[sentenceIndex]?.[partIndex]" class="hint-overlay"
            :style="{ width: `${part.placeholderLength * 0.6}em` }">
            {{ part.correctAnswers.join(' | ') }}
          </div>

          <span v-if="results[textIndex][sentenceIndex][partIndex] !== undefined" class="position-absolute result-icon">
            <font-awesome-icon
              :icon="results[textIndex][sentenceIndex][partIndex] ? ['fas', 'check'] : ['fas', 'xmark']"
              :class="results[textIndex][sentenceIndex][partIndex] ? 'text-success' : 'text-danger'" />
          </span>
        </div>
      </div>
    </div>
    <div v-if="parsedAterWord" class="afterwords-section">
      <hr />
      <div v-html="parsedAterWord"></div>
    </div>

    <div class="d-flex justify-content-between mt-3">
      <div class="btn-group">
        <SpecialCharsButtons @diacrt-click="handleDiacrtButtonClick" />
      </div>
      <div v-if="hasCheck" class="btn-group">
        <HintButton @show-hint="toggleShowHints" />
        <button class="btn btn-outline-primary" @click="checkAnswers" title="Kuotele otviettua">
          <font-awesome-icon :icon="['fas', 'spell-check']" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import SpecialCharsButtons from '@/components/ui/SpecialCharsButtons.vue';
import HintButton from '@/components/ui/HintButtonComponent.vue';
import { confettiMixin } from '@/mixins/confettiMixin.js';

export default {
  name: 'FillBlankTextExercise',
  mixins: [confettiMixin],
  components: {
    SpecialCharsButtons,
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
      isShowHints: false,
      activeTextIndex: null,
      activeSentenceIndex: null,
      activePartIndex: null,
      hintForField: [],
      focusedFields: []
    };
  },
  computed: {
    parsedExample() {
      return this.data.example ? this.parseText([this.data.example]) : [];
    },
    parsedAterWord() {
      return this.data.afterWord ?? null;
    },
    parsedTexts() {
      if (!this.data.texts) {
        return [];
      }
      return this.data.texts.map((textObj) => ({
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
            correctAnswers: match[2].split('|'),
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
      this.hintForField = this.parsedTexts.map((textObj) =>
        textObj.text.map((sentence) =>
          sentence.map(() => false)
        )
      );
      this.focusedFields = this.parsedTexts.map((textObj) =>
        textObj.text.map((sentence) =>
          sentence.map(() => false)
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
    toggleShowHints(show) {
      this.isShowHints = show;

      if (show) {
        this.hintForField = this.parsedTexts.map((textObj) =>
          textObj.text.map((sentence) =>
            sentence.map((part) =>
              part.type === 'blank'
            )
          )
        );
      } else {
        this.hintForField = this.parsedTexts.map((textObj) =>
          textObj.text.map((sentence) =>
            sentence.map(() => false)
          )
        );
      }
    },
    checkAnswers() {
      this.clearResult();
      let allCorrect = true;
      this.parsedTexts.forEach((textObj, textIndex) => {
        textObj.text.forEach((sentence, sentenceIndex) => {
          sentence.forEach((part, partIndex) => {
            if (part.type === 'blank') {
              const userAnswer = this.userAnswers[textIndex][sentenceIndex][partIndex]?.toLowerCase().replaceAll(/['’ʼ]/g, "'");
              const isCorrect = part.correctAnswers.map(ans => ans.toLowerCase().replaceAll(/['’ʼ]/g, "'")).includes(userAnswer);
              this.results[textIndex][sentenceIndex][partIndex] = isCorrect;
              if (!isCorrect) {
                allCorrect = false;
              }
            }
          });
        });
      });
      if (allCorrect) {
        this.launchConfetti();
      }
    },
    handleFocus(textIndex, sentenceIndex, partIndex) {
      this.activeTextIndex = textIndex;
      this.activeSentenceIndex = sentenceIndex;
      this.activePartIndex = partIndex;

      if (!this.focusedFields[textIndex]) {
        this.focusedFields[textIndex] = [];
      }
      if (!this.focusedFields[textIndex][sentenceIndex]) {
        this.focusedFields[textIndex][sentenceIndex] = [];
      }
      this.focusedFields[textIndex][sentenceIndex][partIndex] = true;

      if (this.isShowHints) {
        if (!this.hintForField[textIndex]) {
          this.hintForField[textIndex] = [];
        }
        if (!this.hintForField[textIndex][sentenceIndex]) {
          this.hintForField[textIndex][sentenceIndex] = [];
        }
        this.hintForField[textIndex][sentenceIndex][partIndex] = true;
      }
    },
    handleBlur(textIndex, sentenceIndex, partIndex) {
      if (this.focusedFields[textIndex] && this.focusedFields[textIndex][sentenceIndex]) {
        this.focusedFields[textIndex][sentenceIndex][partIndex] = false;
      }

      if (this.isShowHints) {
        if (this.hintForField[textIndex] && this.hintForField[textIndex][sentenceIndex]) {
          this.hintForField[textIndex][sentenceIndex][partIndex] = false;
        }
      }
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
.sentence {
  justify-content: space-between;
}

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
  position: relative;
  z-index: 1;
}

.result-icon {
  top: 50%;
  transform: translateY(-50%);
  right: 0.1em;
  z-index: 3;
}

.text-center {
  text-align: center;
}
</style>