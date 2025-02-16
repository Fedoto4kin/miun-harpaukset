<template>
    <div class="sentence-assembly-exercise">
        
        <div v-if="examples.length" class="example-container">
            <div class="row align-items-center" v-for="(example, i) in examples" :key="i">
                <div class="col-1"></div>
                <div class="col" v-for="(word, j) in example" :key="j">
                    <span class="word-slot card bg-light text-center bg-white">
                        {{ word ? word : '&nbsp;' }}
                    </span>
                </div>
                <div class="col-1">&nbsp;</div>
            </div>
        </div>

        <div v-for="(slot, sentenceIndex) in slots" :key="sentenceIndex"
            class="row mt-1 align-items-center position-relative">
            <div class="col-1 text-right">
                <span class="badge badge-secondary bg-secondary">{{ sentenceIndex + 1 }}</span>
            </div>
            <div class="col" v-for="(word, slotIndex) in slot" :key="slotIndex"
                @click="!isPrefilled(sentenceIndex, slotIndex) && setActiveSlot(sentenceIndex, slotIndex,)">
                <span :class="{
                    'word-slot card bg-light text-center': true,
                    'active-slot': isActiveSlot(sentenceIndex, slotIndex),
                    'text-success': checkResult && isCorrectWord(sentenceIndex, slotIndex),
                    'text-danger': checkResult && !isCorrectWord(sentenceIndex, slotIndex) && word,
                    'prefilled': isPrefilled(sentenceIndex, slotIndex),
                }">
                    {{ word ? word : '&nbsp;' }}
                </span>
            </div>
            <div class="col-1">
                <button class="btn btn-link btn-clear btn-sm"
                    :class="{ 'text-black': isRowFilled(sentenceIndex), 'text-secondary': !isRowFilled(sentenceIndex) }"
                    :disabled="!isRowFilled(sentenceIndex)" @click="clearSlot(sentenceIndex)">
                    <font-awesome-icon :icon="['fas', 'delete-left']" />
                </button>
            </div>
            <span v-if="checkResult && results[sentenceIndex] !== undefined" class="position-absolute result-icon">
                <font-awesome-icon :icon="results[sentenceIndex].correct ? ['fas', 'check'] : ['fas', 'xmark']"
                    :class="results[sentenceIndex].correct ? 'text-success' : 'text-danger'" />
            </span>
        </div>

        <div class="chioses-container mt-4">
            <div class="mb-2" v-for="(group, groupIndex) in groups" :key="groupIndex">
                <div class="words-container">
                    <button v-for="(word, wordIndex) in group.words" :key="wordIndex"
                        @click="selectWord(groupIndex, wordIndex)" :disabled="word.disabled"
                        class="btn btn-outline-secondary btn-sm" v-html="word.text">
                    </button>
                </div>
            </div>
        </div>


        <div class="d-flex flex-row-reverse mt-1">
            <button class="btn btn-outline-primary" @click="checkAnswers" title="Kuotele otviettua">
                <font-awesome-icon :icon="['fas', 'spell-check']" />
            </button>
        </div>
    </div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

export default {
    name: 'SentenceAssemblyPrefilledExercise',
    components: {
        FontAwesomeIcon
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
            slots: [],
            results: [],
            activeSlot: { sentenceIndex: null, slotIndex: null },
            checkResult: false,
        };
    },
    computed: {
        groups() {
            return this.data?.groups?.map((group) => ({
                ...group,
                words: group.words.map((word) => ({
                    text: word,
                    disabled: false,
                })),
            })) || [];
        },
        answers() {
            console.log(this.data.answers);
            return this.data?.answers || [];
        },
        template() {
            return this.data?.template || {};
        },
        examples() {
            return this.data.template.examples ? this.data.template.examples : [];
        },
    },
    methods: {
        initializeSlots() {
            this.slots = Array.from({ length: this.template.count }, (_, i) =>
                this.template.prefillers && this.template.prefillers[i]
                    ? [...this.template.prefillers[i]]
                    : Array(this.template.slots).fill('')
            );

            // По умолчанию устанавливаем активный слот на первый свободный
            let nextSentenceIndex = 0;
            let nextSlotIndex = 0;

            while (nextSentenceIndex < this.slots.length) {
                if (this.slots[nextSentenceIndex]) {
                    if (nextSlotIndex < this.slots[nextSentenceIndex].length) {
                        if (!this.slots[nextSentenceIndex][nextSlotIndex]) {
                            this.activeSlot = { sentenceIndex: nextSentenceIndex, slotIndex: nextSlotIndex };
                            return;
                        }
                        nextSlotIndex++;
                    } else {
                        nextSentenceIndex++;
                        nextSlotIndex = 0;
                    }
                } else {
                    nextSentenceIndex++;
                    nextSlotIndex = 0;
                }
            }

            // Если пустые слоты не найдены, устанавливаем значение по умолчанию
            this.activeSlot = { sentenceIndex: null, slotIndex: null };
        },

        setFirstAvailableSlot() {
            let nextSentenceIndex = this.activeSlot ? this.activeSlot.sentenceIndex : 0;
            let nextSlotIndex = this.activeSlot ? this.activeSlot.slotIndex + 1 : 0;

            while (nextSentenceIndex < this.slots.length) {
                if (this.slots[nextSentenceIndex]) {
                    if (nextSlotIndex < this.slots[nextSentenceIndex].length) {
                        if (!this.slots[nextSentenceIndex][nextSlotIndex]) {
                            this.activeSlot = { sentenceIndex: nextSentenceIndex, slotIndex: nextSlotIndex };
                            return;
                        }
                        nextSlotIndex++;
                    } else {
                        nextSentenceIndex++;
                        nextSlotIndex = 0;
                    }
                } else {
                    nextSentenceIndex++;
                    nextSlotIndex = 0;
                }
            }
            for (let sentenceIndex = 0; sentenceIndex < this.slots.length; sentenceIndex++) {
                if (this.slots[sentenceIndex]) {
                    for (let slotIndex = 0; slotIndex < this.slots[sentenceIndex].length; slotIndex++) {
                        if (!this.slots[sentenceIndex][slotIndex]) {
                            this.activeSlot = { sentenceIndex, slotIndex };
                            return;
                        }
                    }
                }
            }
            this.activeSlot = { sentenceIndex: null, slotIndex: null };
        },
        setActiveSlot(sentenceIndex, slotIndex) {
            if (this.slots[sentenceIndex] && this.slots[sentenceIndex][slotIndex] !== undefined) {
                this.activeSlot = { sentenceIndex, slotIndex };
            }
        },
        isActiveSlot(sentenceIndex, slotIndex) {
            return (
                this.activeSlot.sentenceIndex === sentenceIndex &&
                this.activeSlot.slotIndex === slotIndex &&
                this.slots[sentenceIndex] &&
                this.slots[sentenceIndex][slotIndex] !== undefined
            );
        },
        isRowFilled(sentenceIndex) {
            return this.slots[sentenceIndex]?.some((slot) => slot);
        },
        selectWord(groupIndex, wordIndex) {
            this.checkResult = false;

            const word = this.groups[groupIndex]
                ?.words[wordIndex]
                ?.text
                .replace(/<\/?[^>]+(>|$)/g, "");

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
                this.setFirstAvailableSlot();
            }
        },
        clearSlot(sentenceIndex) {
            this.checkResult = false;

            this.slots[sentenceIndex].forEach((word, slotIndex) => {
                if (word && (!this.template.prefillers || !this.template.prefillers[sentenceIndex] || !this.template.prefillers[sentenceIndex][slotIndex])) {
                    this.slots[sentenceIndex][slotIndex] = '';
                }
            });

            for (let slotIndex = 0; slotIndex < this.slots[sentenceIndex].length; slotIndex++) {
                if (!this.slots[sentenceIndex][slotIndex]) {
                    this.activeSlot = { sentenceIndex, slotIndex };
                    return;
                }
            }
        },
        isCorrectWord(sentenceIndex, slotIndex) {
            if (!this.results[sentenceIndex] || !this.results[sentenceIndex].correctWords) {
                return false;
            }
            return this.results[sentenceIndex].correctWords[slotIndex];
        },
        isPrefilled(sentenceIndex, slotIndex) {
            return this.template && this.template.prefillers[sentenceIndex][slotIndex] !== '';
        },
        checkAnswers() {
            this.results = this.slots.map((slot) => {
                let correctWords = Array(slot.length).fill(false);
                let isCorrect = false;

                for (let answer of this.answers) {
                    const answerWords = answer.split('|');

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
        if (this.data) {
            this.initializeSlots();
        }
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
    cursor: pointer;
}

.active-slot {
    border: 2px solid blue;
}

.prefilled {
    background-color: white !important;
    color: black !important;
}


.result-icon {
    width: 1.5em;
    top: 50%;
    right: 4em;
    transform: translateY(-50%);
}
</style>