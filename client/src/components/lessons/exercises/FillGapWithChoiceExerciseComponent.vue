<template>
    <div class="fill-gap-with-choice-exercise">
        <div v-for="(question, index) in questions" :key="index" class="mb-2">
            <div class="d-inline-flex flex-wrap question-text mb-1">
                <span v-for="(part, partIndex) in getQuestionParts(question)" :key="partIndex">
                    <span v-if="part.isGap" class="form-control mx-1 input-field">
                        {{ getGapContent(question) }} <!-- todo: hint tooltip-->
                    </span>
                    <span v-else>
                        {{ part.text }}
                    </span>
                </span>
            </div>
            <div class="variants">
                <button v-for="(variant, variantIndex) in question.variants" :key="variantIndex"
                    class="btn btn-outline-secondary btn-sm" :disabled="isVariantSelected(question, variant)"
                    @click="selectVariant(question, variant)">
                    {{ variant }}
                </button>
            </div>
        </div>
        <div class="d-flex justify-content-end mt-2">
            <div v-if="hasCheck" class="btn-group">
                <HintButton @show-hint="isShowHints = $event" />
                <button class="btn btn-outline-primary" @click="checkAnswers" title="Kuotele otviettua">
                    <font-awesome-icon :icon="['fas', 'spell-check']" />
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import HintButton from '@/components/ui/HintButtonCompponent.vue';

export default {
    name: 'FillGapWithChoiceExercise',
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
            default: true,
        },
    },
    data() {
        return {
            questions: this.data.questions || [],
            selectedVariants: {},
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
            const match = question.text.match(/\[\*(\d+):/);
            return match ? parseInt(match[1], 10) : 4;
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
        },

        checkAnswers() {
            // todo
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
</style>