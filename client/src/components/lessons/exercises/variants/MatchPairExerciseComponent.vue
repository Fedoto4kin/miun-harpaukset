<template>
  <div class="match-pair-exercise">
    <!-- Заголовок упражнения -->
    <h5 v-if="data.title" class="exercise-title mb-3">
      {{ data.title }}
    </h5>

    <div v-for="(question, questionIndex) in data.questions" :key="questionIndex" class="words-pairs-container">
      <div class="words-container">
        <div v-for="(word, index) in shuffledWords[questionIndex]" :key="index"
          class="d-flex align-items-center mb-2 position-relative">
          <button class="btn btn-outline-secondary btn-sm word-button me-2" @click="selectWord(questionIndex, index)"
            :class="{ 'btn-selected': selectedWordIndex === index && selectedQuestionIndex === questionIndex }">
            {{ word }}
          </button>
          <div class="input-group pair-slot-container position-relative input-wrapper">
            <span :style="{
              minWidth: `${longestPairLength}em`,
              color: results[questionIndex][index] === undefined ? 'black' : results[questionIndex][index] ? 'green' : 'red'
            }" class="pair-slot bg-light form-control">
              {{ userAnswers[questionIndex][index] ? userAnswers[questionIndex][index] : '&nbsp;' }}
            </span>

            <!-- Подсказка поверх слота -->
            <div v-if="isShowHints && hintForField[questionIndex]?.[index]" class="hint-overlay"
              :style="{ minWidth: `${longestPairLength}em` }">
              {{ getCorrectPair(word, questionIndex) }}
            </div>

            <div class="input-group-append">
              <button class="btn btn-link btn-clear btn-sm"
                :class="{ 'text-black': !!userAnswers[questionIndex][index], 'text-secondary': !userAnswers[questionIndex][index] }"
                :disabled="!userAnswers[questionIndex][index]" @click="clearSlot(questionIndex, index)">
                <font-awesome-icon :icon="['fas', 'delete-left']" />
              </button>
            </div>
            <span v-if="results[questionIndex][index] !== undefined" class="position-absolute result-icon">
              <font-awesome-icon :icon="results[questionIndex][index] ? ['fas', 'check'] : ['fas', 'xmark']"
                :class="results[questionIndex][index] ? 'text-success' : 'text-danger'" />
            </span>
          </div>
        </div>
      </div>
    </div>
    <div class="divider mt-1">
      <hr />
    </div>

    <div class="fixed-height pairs-container mt-3">
      <div class="pairs-container">
        <button v-for="(pair, index) in shuffledPairs" :key="index" class="btn btn-outline-secondary btn-sm pair-button"
          @click="selectPair(index)" :disabled="!pairsEnabled || isPairSelected(index)">
          {{ pair }}
        </button>
      </div>
    </div>

    <div class="d-flex justify-content-end mt-2">
      <div class="btn-group">
        <HintButton @show-hint="toggleShowHints" />
        <button class="btn btn-outline-primary" @click="checkAnswers" title="Kuotele otviettua">
          <font-awesome-icon :icon="['fas', 'spell-check']" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import HintButton from '@/components/ui/HintButtonComponent.vue';
import { confettiMixin } from '@/mixins/confettiMixin.js';

export default {
  name: 'MatchPairExercise',
  mixins: [confettiMixin],
  components: {
    HintButton
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
      selectedQuestionIndex: 0,
      selectedWordIndex: 0,
      selectedPairIndex: null,
      checkResult: false,
      shuffledWords: [],
      shuffledPairs: [],
      userAnswers: [],
      isShowHints: false,
      pairsEnabled: true,
      results: [],
      hintForField: [],
      focusedSlots: []
    };
  },
  computed: {
    longestPairLength() {
      const allPairs = this.data.questions.flatMap(question => question.pairs.map(pair => pair.pair));
      return Math.max(...allPairs.map(pair => pair.length)) * 0.8;
    },
  },
  methods: {
    initializeAnswers() {
      this.userAnswers = this.data.questions.map(question => Array(question.pairs.length).fill(''));
      this.shuffledWords = this.data.questions.map(question => this.shuffleArray(question.pairs.map(pair => pair.word)));
      this.shuffleData();
    },
    shuffleData() {
      this.shuffledWords = this.data.questions.map(question => this.shuffleArray(question.pairs.map(pair => pair.word)));
      const allPairs = this.data.questions.flatMap(question => question.pairs.map(pair => pair.pair));
      this.shuffledPairs = this.shuffleArray(allPairs);
    },
    shuffleArray(array) {
      const shuffledArray = array.slice();
      for (let i = shuffledArray.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffledArray[i], shuffledArray[j]] = [shuffledArray[j], shuffledArray[i]];
      }
      return shuffledArray;
    },
    selectWord(questionIndex, index) {
      this.selectedQuestionIndex = questionIndex;
      this.selectedWordIndex = index;
      this.pairsEnabled = true;

      // Показываем подсказку для выбранного слота, если включены подсказки
      if (this.isShowHints) {
        this.updateHintsForSlot(questionIndex, index);
      }

      this.resetResults();
    },
    selectPair(index) {
      if (this.selectedWordIndex !== null) {
        const currentPair = this.userAnswers[this.selectedQuestionIndex][this.selectedWordIndex];
        if (currentPair) {
          this.shuffledPairs.push(currentPair);
        }

        this.userAnswers[this.selectedQuestionIndex][this.selectedWordIndex] = this.shuffledPairs[index];
        this.shuffledPairs.splice(index, 1);

        let nextEmptySlotIndex = null;

        for (let i = this.selectedWordIndex + 1; i < this.userAnswers[this.selectedQuestionIndex].length; i++) {
          if (this.userAnswers[this.selectedQuestionIndex][i] === '') {
            nextEmptySlotIndex = i;
            break;
          }
        }

        if (nextEmptySlotIndex === null) {
          nextEmptySlotIndex = this.userAnswers[this.selectedQuestionIndex].findIndex(answer => answer === '');
        }

        if (nextEmptySlotIndex === -1) {
          for (let i = this.selectedQuestionIndex + 1; i < this.userAnswers.length; i++) {
            nextEmptySlotIndex = this.userAnswers[i].findIndex(answer => answer === '');
            if (nextEmptySlotIndex !== -1) {
              this.selectedQuestionIndex = i;
              break;
            }
          }
        }

        if (nextEmptySlotIndex === -1) {
          for (let i = 0; i <= this.selectedQuestionIndex; i++) {
            nextEmptySlotIndex = this.userAnswers[i].findIndex(answer => answer === '');
            if (nextEmptySlotIndex !== -1) {
              this.selectedQuestionIndex = i;
              break;
            }
          }
        }

        if (nextEmptySlotIndex !== -1) {
          this.selectedWordIndex = nextEmptySlotIndex;

          // Показываем подсказку для нового выбранного слота, если включены подсказки
          if (this.isShowHints) {
            this.updateHintsForSlot(this.selectedQuestionIndex, nextEmptySlotIndex);
          }
        } else {
          this.pairsEnabled = false;
        }
      }
      this.resetResults();
    },
    clearSlot(questionIndex, index) {
      const removedPair = this.userAnswers[questionIndex][index];
      if (removedPair) {
        this.shuffledPairs.push(removedPair);
        this.userAnswers[questionIndex][index] = '';
        this.selectedQuestionIndex = questionIndex;
        this.selectedWordIndex = index;
        this.pairsEnabled = true;

        // Показываем подсказку для очищенного слота, если включены подсказки
        if (this.isShowHints) {
          this.updateHintsForSlot(questionIndex, index);
        }
      }
      this.resetResults();
    },

    isWordSelected(questionIndex, index) {
      return !!this.userAnswers[questionIndex][index];
    },
    isPairSelected(index) {
      return this.userAnswers.flat().includes(this.shuffledPairs[index]);
    },
    checkAnswers() {
      this.resetResults();
      let allCorrect = true;
      this.results = this.userAnswers.map((answers, questionIndex) =>
        answers.map((answer, index) => {
          const pair = this.data.questions[questionIndex].pairs.find(pair => pair.word === this.shuffledWords[questionIndex][index]);
          const isCorrect = pair && pair.pair === answer;
          if (!isCorrect) {
            allCorrect = false;
          }
          return isCorrect;
        })
      );
      this.checkResult = true;

      if (allCorrect) {
        this.launchConfetti();
      }
    },

    resetResults() {
      this.checkResult = false;
      this.results = [];
      this.results = this.data.questions.map(() => Array(this.data.questions[0].pairs.length).fill(undefined));
    },

    getCorrectPair(word, questionIndex) {
      const pair = this.data.questions[questionIndex].pairs.find(pair => pair.word === word);
      return pair ? pair.pair : '';
    },
    toggleShowHints(show) {
      this.isShowHints = show;

      if (show) {
        // Показываем подсказки для ВСЕХ слотов
        this.hintForField = this.data.questions.map((question) =>
          Array(question.pairs.length).fill(true)
        );
      } else {
        // Скрываем все подсказки
        this.hintForField = this.data.questions.map(() => []);
      }
    },

    updateHintsForSlot(questionIndex, slotIndex) {
      if (!this.hintForField[questionIndex]) {
        this.hintForField[questionIndex] = [];
      }

      // Сбрасываем все подсказки
      this.hintForField = this.data.questions.map(() => []);

      // Показываем подсказку только для текущего слота
      if (!this.hintForField[questionIndex]) {
        this.hintForField[questionIndex] = [];
      }
      this.hintForField[questionIndex][slotIndex] = true;
    }
  },
  created() {
    this.initializeAnswers();
    this.resetResults();
    this.hintForField = this.data.questions.map(() => []);
    this.focusedSlots = this.data.questions.map(() => []);
  }
};
</script>

<style scoped>
.exercise-title {
  color: #2c3e50;
  font-weight: 600;
}

.words-pairs-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.words-container,
.pairs-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  justify-content: center;
}

.pairs-container.fixed-height {
  min-height: 2.5em;
  align-items: flex-start;
}

.word-button,
.pair-button {
  text-align: left;
  white-space: nowrap;
}

.word-button.btn-selected {
  background-color: #e9f5ff;
  border-color: #007bff;
}

.word-button.btn-selected:hover {
  background-color: rgba(var(--bs-secondary-rgb)) !important;
}

.pair-slot-container {
  display: flex;
  align-items: center;
}

.pair-slot {
  border: 1px dashed #ddd !important;
  padding: 0.25rem 0.5rem;
  text-align: center;
  margin-right: 0.5rem;
  position: relative;
  z-index: 1;
}

.divider {
  width: 100%;
  text-align: center;
}

.result-icon {
  width: 1.5em;
  top: 50%;
  right: 1.0em;
  transform: translateY(-50%);
  z-index: 3;
}
</style>