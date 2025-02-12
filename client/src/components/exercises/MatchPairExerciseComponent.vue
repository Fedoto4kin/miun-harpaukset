<template>
    <div class="match-pair-exercise">
    
      <div class="words-pairs-container">
        <div class="words-container">
          <div
            v-for="(word, index) in shuffledWords"
            :key="index"
            class="d-flex align-items-center mb-2 position-relative"
          >
            <button
              class="btn btn-outline-secondary btn-sm word-button me-2"
              @click="selectWord(index)"
              :class="{ 'btn-selected': selectedWordIndex === index }"
            >
              {{ word }}
            </button>
            <div class="input-group pair-slot-container"
                    v-tooltip="{
                        content: getCorrectPair(word),
                        shown: isShowHints,
                        triggers: [],
                        delay: 0
                    }"
                >
              <span
                :style="{
                  minWidth: `${longestPairLength }em`,
                  color: results[index] === undefined ? 'black' : results[index] ? 'green' : 'red'
                }"
                class="pair-slot bg-light form-control"
              >
                {{ userAnswers[index]? userAnswers[index] : '&nbsp;' }}
              </span>
              <div class="input-group-append">
                <button
                  class="btn btn-link btn-clear btn-sm"
                  :class="{'text-black': !!userAnswers[index], 'text-secondary': !userAnswers[index]}"
                  :disabled="!userAnswers[index]"
                  @click="clearSlot(index)"
                >
                  <font-awesome-icon :icon="['fas', 'delete-left']" />
                </button>
              </div>
              <span
                v-if="results[index] !== undefined"
                class="position-absolute result-icon"
              >
                <font-awesome-icon
                  :icon="results[index] ? ['fas', 'check'] : ['fas', 'xmark']"
                  :class="results[index] ? 'text-success' : 'text-danger'"
                />
              </span>
            </div>
          </div>
        </div>
     </div>
     <div class="divider mt-1"><hr /></div>

    <div class="fixed-height pairs-container mt-3">
        <div class="pairs-container">
                <button
                    v-for="(pair, index) in shuffledPairs"
                    :key="index"
                    class="btn btn-outline-secondary btn-sm pair-button"
                    @click="selectPair(index)"
                    :disabled="!pairsEnabled || isPairSelected(index)"
                >
                    {{ pair }}
                </button>
        </div>
    </div>

    <div class="d-flex justify-content-end mt-2">
        <div class="btn-group">
            <HintButton @show-hint="isShowHints = $event" />
            <button 
                class="btn btn-outline-primary"
                @click="checkAnswers"
                title="Kuotele otviettua"
                >
                <font-awesome-icon :icon="['fas', 'spell-check']" />
            </button>
      </div>
    </div>
      
    </div>
  </template>
  
  <script>
  import HintButton from '@/components/ui/HintButtonCompponent.vue';
  
  export default {
    name: 'MatchPairExercise',
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
        selectedWordIndex: 0,
        selectedPairIndex: null,
        checkResult: false,
        shuffledWords: [],
        shuffledPairs: [],
        userAnswers: [],
        isShowHints: false,
        pairsEnabled: true, 
        results: [],
      };
    },
    computed: {
      longestPairLength() {
        return Math.max(...this.data.questions[0].pairs.map(pair => pair.pair.length)) * 0.8;
      },
    },
    methods: {
        initializeAnswers() {
            this.userAnswers = Array(this.data.questions[0].pairs.length).fill('');
            this.shuffleData();
        },
        shuffleData() {
            const words = this.data.questions[0].pairs.map(pair => pair.word);
            const pairs = this.data.questions[0].pairs.map(pair => pair.pair);

            this.shuffledWords = this.shuffleArray(words);
            this.shuffledPairs = this.shuffleArray(pairs);
        },
        shuffleArray(array) {
            const shuffledArray = array.slice();
            for (let i = shuffledArray.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffledArray[i], shuffledArray[j]] = [shuffledArray[j], shuffledArray[i]];
            }
            return shuffledArray;
        },
        selectWord(index) {
            this.selectedWordIndex = index;
            this.pairsEnabled = true;
            this.resetResults(); // Сбросить результаты проверки при выборе нового слова
        },
        selectPair(index) {
            if (this.selectedWordIndex !== null) {
            const currentPair = this.userAnswers[this.selectedWordIndex];
            if (currentPair) {
                this.shuffledPairs.push(currentPair);
            }

            this.userAnswers[this.selectedWordIndex] = this.shuffledPairs[index];
            this.shuffledPairs.splice(index, 1);

            const nextEmptySlotIndex = this.userAnswers.findIndex(answer => answer === '');
            if (nextEmptySlotIndex !== -1) {
                this.selectedWordIndex = nextEmptySlotIndex;
            } else {
                this.pairsEnabled = false;    
            }
            }
            this.resetResults(); // Сбросить результаты проверки при выборе новой пары
        },
        clearSlot(index) {
            const removedPair = this.userAnswers[index];
            if (removedPair) {
            this.shuffledPairs.push(removedPair);
            this.userAnswers[index] = '';
            this.selectedWordIndex = index;
            this.pairsEnabled = true;
            }
            this.resetResults();
        },
        isWordSelected(index) {
            return !!this.userAnswers[index];
        },
        isPairSelected(index) {
            return !this.shuffledPairs.includes(this.shuffledPairs[index]);
        },
        checkAnswers() {
            this.results = this.userAnswers.map((answer, index) => {
            const pair = this.data.questions[0].pairs.find(pair => pair.word === this.shuffledWords[index]);
            return pair && pair.pair === answer;
            });
            this.checkResult = true;
        },
        resetResults() {
            this.checkResult = false;
            this.results = [];
        },
        getCorrectPair(word) {
            const pair = this.data.questions[0].pairs.find(pair => pair.word === word);
            return pair ? pair.pair : '';
        }
    },
    created() {
      this.initializeAnswers();
    },
  };
  </script>
  
  <style scoped>
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
    min-height: 5em;
    align-items: flex-start;
  }
  
  .word-button,
  .pair-button {
    text-align: left;
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
  }
  </style>
  