<template>
  <div class="sentence-assembly-exercise">

    <div class="mb-2" v-for="(group, groupIndex) in groups" :key="groupIndex">
      <div class="words-container">
        <button
          v-for="(word, wordIndex) in group.words"
          :key="wordIndex"
          @click="selectWord(groupIndex, wordIndex)"
          :disabled="word.disabled"
          class="btn btn-outline-secondary btn-sm"
        >
          {{ word.text }}
        </button>
      </div>
    </div>
    <div
      v-for="(slot, sentenceIndex) in slots"
      :key="sentenceIndex"
      class="row mt-1 align-items-center position-relative"
    >
      <div class="col-1 text-right">
        <span class="badge badge-secondary bg-secondary">{{ sentenceIndex + 1 }}</span>
      </div>
      <div
        class="col"
        v-for="(word, slotIndex) in slot"
        :key="slotIndex"
        @click="setActiveSlot(sentenceIndex, slotIndex)"
      >
        <span
          :class="{
            'word-slot card bg-light text-center': true,
            'active-slot': isActiveSlot(sentenceIndex, slotIndex),
            'text-success': checkResult && isCorrectWord(sentenceIndex, slotIndex),
            'text-danger': checkResult && !isCorrectWord(sentenceIndex, slotIndex) && word,
          }"
        >
          {{ word ? word : '&nbsp;' }}
        </span>
      </div>
      <div class="col-1">
        <button
          class="btn btn-link btn-clear btn-sm"
          :class="{'text-black': isRowFilled(sentenceIndex), 'text-secondary': !isRowFilled(sentenceIndex)}"
          :disabled="!isRowFilled(sentenceIndex)"
          @click="clearSlot(sentenceIndex)"
        >
          <font-awesome-icon :icon="['fas', 'delete-left']" />
        </button>
      </div>
      <span
        v-if="checkResult && results[sentenceIndex] !== undefined"
        class="position-absolute result-icon"
      >
        <font-awesome-icon
          :icon="results[sentenceIndex].correct ? ['fas', 'check'] : ['fas', 'xmark']"
          :class="results[sentenceIndex].correct ? 'text-success' : 'text-danger'"
        />
      </span>
    </div>
    <div class="d-flex flex-row-reverse mt-3">
      <button
        class="btn btn-outline-primary"
        @click="checkAnswers"
        title="Kuotele otviettua"
      >
        <font-awesome-icon :icon="['fas', 'spell-check']" />
      </button>
    </div>
  </div>
</template>

<script>

export default {
  name: 'SentenceAssemblyExercise',
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
      slots: [],
      results: [],
      activeSlot: { sentenceIndex: null, slotIndex: null },
      checkResult: false,
    };
  },
  computed: {
    groups() {
      return this.data.groups.map((group) => ({
        ...group,
        words: group.words.map((word) => ({
          text: word,
          disabled: false,
        })),
      }));
    },
    answers() {
      return this.data.answers;
    },
    template() {
      return this.data.template;
    },
  },
  methods: {
    initializeSlots() {
      this.slots = Array.from({ length: this.template.count }, () =>
        Array(this.template.slots).fill('')
      );
      this.setFirstAvailableSlot();
    },
    setFirstAvailableSlot() {
      for (let sentenceIndex = 0; sentenceIndex < this.slots.length; sentenceIndex++) {
        for (let slotIndex = 0; slotIndex < this.slots[sentenceIndex].length; slotIndex++) {
          if (!this.slots[sentenceIndex][slotIndex]) {
            this.activeSlot = { sentenceIndex, slotIndex };
            return;
          }
        }
      }
    },
    setActiveSlot(sentenceIndex, slotIndex) {
      this.activeSlot = { sentenceIndex, slotIndex };
    },
    isActiveSlot(sentenceIndex, slotIndex) {
      return (
        this.activeSlot.sentenceIndex === sentenceIndex &&
        this.activeSlot.slotIndex === slotIndex
      );
    },
    isRowFilled(sentenceIndex) {
      return this.slots[sentenceIndex].some((slot) => slot);
    },
    selectWord(groupIndex, wordIndex) {
      this.checkResult = false;

      const word = this.groups[groupIndex].words[wordIndex].text;

      if (
        this.activeSlot.sentenceIndex !== null &&
        this.activeSlot.slotIndex !== null
      ) {
        const { sentenceIndex, slotIndex } = this.activeSlot;
        if (this.slots[sentenceIndex][slotIndex]) {
          const previousWord = this.slots[sentenceIndex][slotIndex];
          const previousGroupIndex = this.groups.findIndex((group) =>
            group.words.some((w) => w.text === previousWord)
          );
          const previousWordIndex = this.groups[previousGroupIndex].words.findIndex(
            (w) => w.text === previousWord
          );
          this.groups[previousGroupIndex].words[previousWordIndex].disabled = false;
        }
        this.slots[sentenceIndex][slotIndex] = word;
        this.groups[groupIndex].words[wordIndex].disabled = true;
        this.setFirstAvailableSlot();
      }
    },
    clearSlot(sentenceIndex) {
      this.checkResult = false;

      this.slots[sentenceIndex].forEach((word) => {
        if (word) {
          const groupIndex = this.groups.findIndex((group) =>
            group.words.some((w) => w.text === word)
          );
          const wordIndex = this.groups[groupIndex].words.findIndex(
            (w) => w.text === word
          );
          if (groupIndex !== -1 && wordIndex !== -1) {
            this.groups[groupIndex].words[wordIndex].disabled = false;
          }
        }
      });
      this.slots[sentenceIndex] = Array(this.template.slots).fill('');
      this.setFirstAvailableSlot();
    },
    isCorrectWord(sentenceIndex, slotIndex) {
      if (!this.results[sentenceIndex]) {
        return false;
      }
      return this.results[sentenceIndex].correctWords[slotIndex];
    },
    checkAnswers() {
      this.results = this.slots.map((slot) => {
        let correctWords = Array(slot.length).fill(false);
        let isCorrect = false;

        for (let answer of this.answers) {
          const answerWords = answer.split(' ');

          for (let i = 0; i < slot.length; i++) {
            if (slot[i] === answerWords[i] && slot.slice(0, i + 1).every((word, index) => word === answerWords[index])) {
              correctWords[i] = true;
            } else {
              break;
            }
          }
        }

        isCorrect = correctWords.every(Boolean);

        return {
          correctWords,
          correct: isCorrect,
        };
      });
      this.checkResult = true;
    },
  },
  created() {
    this.initializeSlots();
  },
};
</script>

<style scoped>
.words-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.2rem;
  justify-content: left;
}

.word-slot {
    border: 1px dashed #ddd;
    text-align: center;
  }

.active-slot {
  border: 2px solid #007bff !important;
  background-color: #e9f5ff !important;
}

.text-right {
  text-align: right;
}

.result-icon {
  width: 1.5em;
  top: 50%;
  right: 4em;
  transform: translateY(-50%);
}
</style>
