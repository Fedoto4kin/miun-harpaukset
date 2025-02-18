<template>
    <div class="fill-gap-with-choice-exercise">
        <div v-for="(question, questionIndex) in questions" :key="questionIndex" class="mb-2">
            <div class="d-inline-flex flex-wrap question-text mb-1 position-relative">
                <span v-for="(part, partIndex) in getQuestionParts(question)" :key="partIndex">
                    <span v-if="part.isGap" class="form-control mx-1 input-field" 
                          :style="{ color: !checkResult ? 'black' : results[questionIndex] ? 'green' : 'red' }"
                          v-html="selectedVariants[question.text] ? getGapContent(question) : '&nbsp;' "
                          />
                    <span v-else>
                        {{ part.text }}
                    </span>
                    <span v-if="checkResult && results[questionIndex] !== undefined" class="position-absolute result-icon">
                        <font-awesome-icon :icon="results[questionIndex] ? ['fas', 'check'] : ['fas', 'xmark']" :class="results[questionIndex] ? 'text-success' : 'text-danger'" />
                    </span>
                </span>
            </div>
            <div class="variants">
                <button v-for="(variant, variantIndex) in question.variants" :key="variantIndex" class="btn btn-outline-secondary btn-sm" :disabled="isVariantSelected(question, variant)" @click="selectVariant(question, variant)" v-html="variant"></button>
            </div>
        </div>
        <div class="d-flex justify-content-end mt-2">
            <div v-if="hasCheck" class="btn-group">
                <button class="btn btn-outline-primary" @click="checkAnswers" title="Kuotele otviettua">
                    <font-awesome-icon :icon="['fas', 'spell-check']" />
                </button>
            </div>
        </div>
    </div>
</template>


<script>
import { confettiMixin } from '@/mixins/confettiMixin.js';

export default {
    name: 'FillGapWithChoiceExercise',
    mixins: [confettiMixin],
    components: {},
    props: {
        data: {
            type: Object,
            required: true,
        },
        hasCheck: {
            type: Boolean,
            default: true,
        },
    },
    data() {
        return {
            questions: this.data.questions || [],
            selectedVariants: {},
            results: [],
            checkResult: false,
        };
    },
    methods: {
        getQuestionParts(question) {
            const parts = question.text.split(/(\[.*?\])/);
            return parts.map((part) => {
                if (part.startsWith('[') && part.endsWith(']')) {
                    return { text: part, isGap: true };
                } else {
                    return { text: part, isGap: false };
                }
            });
        },

        getGapContent(question) {
            let selected = this.selectedVariants[question.text];
            if (Array.isArray(selected)) {
                return selected.join(', ');
            } else if (selected) {
                return selected;
            } else {
                return ' '.repeat(this.getGapLength(question));
            }
        },

        getGapLength(question) {
            const match = question.text.match(/\[\*\d+:/);
            return match ? parseInt(match[0].match(/\d+/)[0], 10) : 4;
        },

        extractCorrectAnswers(question) {
            const match = question.text.match(/\[\*\d+:([^\]]+)\]/);
            return match ? match[1].split('|') : [];
        },

        isVariantSelected(question, variant) {
            const selected = this.selectedVariants[question.text];
            if (question.type === 'radio') {
                return selected === variant;
            } else if (question.type === 'checkbox') {
                return selected && selected.includes(variant);
            }
            return false;
        },

        selectVariant(question, variant) {
            if (question.type === 'radio') {
                this.selectedVariants[question.text] = variant;
            } else if (question.type === 'checkbox') {
                if (!this.selectedVariants[question.text]) {
                    this.selectedVariants[question.text] = [];
                }
                const index = this.selectedVariants[question.text].indexOf(variant);
                if (index === -1) {
                    this.selectedVariants[question.text].push(variant);
                } else {
                    this.selectedVariants[question.text].splice(index, 1);
                }
            }
            this.checkResult = false;
        },

        checkAnswers() {
            this.results = this.questions.map((question) => {
                const correctAnswers = this.extractCorrectAnswers(question);
                const selected = this.selectedVariants[question.text];
                this.checkResult = true;

                if (question.type === 'radio') {
                    return correctAnswers.includes(selected);
                } else if (question.type === 'checkbox') {
                    return Array.isArray(selected) &&
                        selected.length === correctAnswers.length &&
                        selected.every(variant => correctAnswers.includes(variant));
                } else {
                    // For slot-based answers
                    return correctAnswers.includes(selected);
                }
               
            });

            const allCorrect = this.results.flat().every(result => result === true);
            if (allCorrect) {
                this.launchConfetti();
            }
        },
    },
};
</script>

<style scoped>
.question-text {
    font-size: 1.125em;
}

.input-field {
    display: inline-block;
    width: auto;
    min-width: 1.5em;
    border: none;
    border-bottom: 1px solid #ccc;
    outline: none;
    box-shadow: none;
    padding: 0 5px 0 0.3em;
    font-size: 1em;
    margin: 0 0.2em;
}

.variants {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.variant {
    padding: 5px 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.result-icon {
    width: 1.5em;
    top: 50%;
    right: -1.5em;
    transform: translateY(-50%);
}
</style>
