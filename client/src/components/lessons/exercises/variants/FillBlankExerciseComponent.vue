<template>
  <div class="fill-blank-exercise mt-1">
    <div v-for="(group, groupIndex) in parsedGroups" :key="groupIndex" class="mt-3">
      <div v-if="group.instructions" class="mb-1 text-center">
        <strong>{{ group.instructions }}</strong>
      </div>
      <div class="row justify-content-center">
        <div v-for="(item, itemIndex) in group.questions" :key="itemIndex" class="w-auto mb-2 px-3">
          <div class="card bg-light py-2 px-3 text-center">
            <div class="d-flex justify-content-center align-items-center position-relative">
              <span>{{ item.textBefore }}</span>
              <div class="position-relative input-wrapper">
                <input :ref="'inputField' + groupIndex + '-' + itemIndex" 
                  v-model="userAnswers[groupIndex][itemIndex]"
                  :style="{
                    width: `${item.placeholderLength * 1.1}em`,
                    color: results[groupIndex][itemIndex] === undefined ? 'black' : results[groupIndex][itemIndex] ? 'green' : 'red'
                  }" 
                  class="form-control mx-1 input-field" 
                  @input="checkAnswer(groupIndex, itemIndex)"
                  @focus="handleFocus(groupIndex, itemIndex)" />
                
                <!-- Подсказка поверх поля ввода -->
                <div v-if="isShowHints && hintForField[groupIndex]?.[itemIndex]"
                  class="hint-overlay"
                  :style="{ width: `${item.placeholderLength * 0.8}em` }">
                  <span class="hint-content">
                    {{ getHintDisplay(item.correctAnswers) }}
                  </span>
                </div>
              </div>
              <span v-if="item.textAfter">{{ item.textAfter }}</span>
              <span v-if="results[groupIndex][itemIndex] !== undefined" class="position-absolute result-icon">
                <font-awesome-icon :icon="results[groupIndex][itemIndex] ? ['fas', 'check'] : ['fas', 'xmark']"
                  :class="results[groupIndex][itemIndex] ? 'text-success' : 'text-danger'" />
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="d-flex justify-content-between mt-3">
      <div class="btn-group">
        <SpecialCharsButtons @diacrt-click="handleDiacrtButtonClick" />
      </div>
      <HintButton @show-hint="toggleShowHints" />
    </div>
  </div>
</template>

<script>
import SpecialCharsButtons from '@/components/ui/SpecialCharsButtons.vue';
import HintButton from '@/components/ui/HintButtonComponent.vue';
import { confettiMixin } from '@/mixins/confettiMixin.js';

export default {
  name: 'FillBlankExercise',
  mixins: [confettiMixin],
  components: {
    SpecialCharsButtons,
    HintButton,
  },
  props: {
    data: {
      type: Object,
      required: false,
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
      parsedGroups: [],
      isShowHints: false,
      activeGroupIndex: null,
      activeItemIndex: null,
      hintForField: []
    };
  },
  methods: {
    parseData() {
      const sortedGroups = [...this.data].sort((a, b) => a.order - b.order);

      this.parsedGroups = sortedGroups.map(group => ({
        instructions: group.text ?? null,
        questions: group.questions.map(item => {
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
        })
      }));
    },
    
    checkAnswer(groupIndex, itemIndex) {
      if (this.userAnswers[groupIndex][itemIndex] === '') {
        this.results[groupIndex][itemIndex] = undefined;
        return;
      }
      const correctAnswers = this.parsedGroups[groupIndex].questions[itemIndex].correctAnswers;
      const userAnswer = this.userAnswers[groupIndex][itemIndex].toLowerCase();
      const isCorrect = correctAnswers.includes(userAnswer);
      this.results[groupIndex][itemIndex] = isCorrect;

      const allCorrect = this.results.flat().every(result => result === true);
      if (allCorrect) {
        this.launchConfetti();
      }
    },
    
    getHintDisplay(correctAnswers) {
      return correctAnswers.join(', ');
    },
    
    toggleShowHints(show) {
      this.isShowHints = show;
      
      if (show) {
        this.hintForField = this.parsedGroups.map(() =>
          this.parsedGroups[0].questions.map(() => true)
        );
      } else {
        this.hintForField = this.parsedGroups.map(() => []);
      }
    },

    handleFocus(groupIndex, itemIndex) {
      this.activeGroupIndex = groupIndex;
      this.activeItemIndex = itemIndex;
    },
    
    handleDiacrtButtonClick(event) {
      if (this.activeGroupIndex === null || this.activeItemIndex === null) {
        console.error("No active input field.");
        return;
      }

      const char = event.target.dataset.char;
      const activeElement = this.$refs[`inputField${this.activeGroupIndex}-${this.activeItemIndex}`][0];

      if (activeElement) {
        const position = activeElement.selectionStart;
        const updatedText = [
          activeElement.value.slice(0, position),
          char,
          activeElement.value.slice(position)
        ].join('');
        this.userAnswers[this.activeGroupIndex][this.activeItemIndex] = updatedText;
        this.$nextTick(() => {
          activeElement.focus();
          activeElement.selectionStart = activeElement.selectionEnd = position + 1;
          this.checkAnswer(this.activeGroupIndex, this.activeItemIndex);
        });
      }
    },
  },
  created() {
    this.parseData();
    this.userAnswers = this.parsedGroups.map(group => group.questions.map(() => ''));
    this.results = this.parsedGroups.map(group => group.questions.map(() => undefined));
    this.hintForField = this.parsedGroups.map(() => []);
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
  position: relative;
  z-index: 1;
}

.input-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
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
  right: -1.9em;
  z-index: 3;
}

.text-center {
  text-align: center;
}

.hint-overlay {
  font-size: 1.1em; 
  left: 12%;
  text-align: center;
  pointer-events: none;
  overflow: visible;
  min-height: 100%;
  line-height: 1.5;
  min-width: fit-content;
}

</style>
