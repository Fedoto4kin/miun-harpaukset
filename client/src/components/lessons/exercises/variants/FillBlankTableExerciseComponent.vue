<template>
    <div class="fill-blank-table-exercise">
        <table class="table table-sm align-bottom mb-5" :class="data.class ? data.class : 'table-bordered'">
            <tbody>
                <tr v-for="(row, rowIndex) in data.table" :key="rowIndex">
                    <td v-for="(cell, colIndex) in row" :key="colIndex" :class="cell.class">
                        <template v-for="(fragment, fragmentIndex) in parseContent(cell.content)" :key="fragmentIndex">
                            <span v-if="fragment.type === 'text'" v-html="fragment.value" />
                            <span v-else-if="fragment.type === 'span'" class="form-control mx-1 input-field text-wrap"
                                :style="{ width: `${calculateExampleStringField(fragment.value ?? '')}em` }"
                                v-html="fragment.value ?? '&nbsp;'" />
                            <span v-else class="position-relative">
                                <input v-model="userAnswers[rowIndex][colIndex][fragmentIndex]"
                                    :ref="'inputField' + rowIndex + '-' + colIndex + '-' + fragmentIndex" :style="{
                                        width: `${getPlaceholderLength(fragment.value)}em`,
                                        color: results[rowIndex][colIndex][fragmentIndex] === undefined ? 'black' : results[rowIndex][colIndex][fragmentIndex] ? 'green' : 'red'
                                    }" class="form-control mx-1 input-field" @input="handleInputChange"
                                    @focus="handleFocus(rowIndex, colIndex, fragmentIndex)" v-tooltip.right="{
                                        content: getCorrectAnswers(fragment.value).join(', '),
                                        shown: isShowHints,
                                        triggers: [],
                                        delay: 0,
                                    }" />
                                <span v-if="results[rowIndex][colIndex][fragmentIndex] !== undefined"
                                    class="position-absolute result-icon">
                                    <font-awesome-icon
                                        :icon="results[rowIndex][colIndex][fragmentIndex] ? ['fas', 'check'] : ['fas', 'xmark']"
                                        :class="results[rowIndex][colIndex][fragmentIndex] ? 'text-success' : 'text-danger'" />
                                </span>
                            </span>
                        </template>
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="d-flex justify-content-between mt-3">
            <div class="btn-group">
                <SpecialCharsButtons @diacrt-click="handleDiacrtButtonClick" />
            </div>
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
import SpecialCharsButtons from '@/components/ui/SpecialCharsButtons.vue';
import HintButton from '@/components/ui/HintButtonComponent.vue';
import { confettiMixin } from '@/mixins/confettiMixin.js';

export default {
    name: 'FillBlankTableExerciseComponent',
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
            activeRowIndex: null,
            activeColIndex: null,
            activeFragmentIndex: null,
        };
    },
    methods: {
        calculateExampleStringField(exampleString) {
            return exampleString.replace(/<\/?[^>]+(>|$)/g, "").length * 0.7;
        },
        getPlaceholderLength(content) {
            const match = content.match(/\[(\d+)\*:/);
            return match ? Number(match[1]) + 2 : content.length;
        },
        getCorrectAnswers(content) {
            const match = content.match(/\[(\d+)\*:([^\]{]+)\]/);
            return match ? match[2].split('|') : [];
        },
        parseContent(content) {
            if (!content) {
                return [];
            }

            const fragments = [];
            let remainingContent = content;
            const regex = /\[(\d+)\*:([^\]{]+)\]|\{([^}]+)}/g;
            let match;

            while ((match = regex.exec(remainingContent)) !== null) {
                const textBefore = remainingContent.slice(0, match.index);
                if (textBefore.length > 0) {
                    fragments.push({ type: 'text', value: textBefore });
                }

                if (match[1]) { // Обработка разметки []
                    fragments.push({ type: 'input', value: match[0] });
                } else if (match[3]) { // Обработка разметки {}
                    fragments.push({ type: 'span', value: match[3] });
                }

                remainingContent = remainingContent.slice(match.index + match[0].length);
            }

            if (remainingContent.length > 0) {
                fragments.push({ type: 'text', value: remainingContent });
            }

            return fragments;
        },



        parseData() {
            this.userAnswers = this.data.table.map(row =>
                row.map(cell =>
                    this.parseContent(cell.content).map(fragment =>
                        fragment.type === 'input' ? '' : fragment.value
                    )
                )
            );
            this.results = this.data.table.map(row =>
                row.map(() =>
                    this.parseContent(row.content).map(() => undefined)
                )
            );
        },
        clearResult() {
            this.results = this.data.table.map(row =>
                row.map(() =>
                    this.parseContent(row.content).map(() => undefined)
                )
            );
        },
        checkAnswers() {
            this.clearResult();
            this.data.table.forEach((row, rowIndex) => {
                row.forEach((cell, colIndex) => {
                    this.parseContent(cell.content).forEach((fragment, fragmentIndex) => {
                        if (fragment.type === 'input') {
                            const userAnswer = this.userAnswers[rowIndex][colIndex][fragmentIndex]
                                ?.toLowerCase()
                                .replaceAll(/['’ʼ]/g, "'");
                            console.log(`User answer for row ${rowIndex}, col ${colIndex}, fragment ${fragmentIndex}: ${userAnswer}`);

                            const correctAnswers = this.getCorrectAnswers(fragment.value).map(ans =>
                                ans.toLowerCase().replaceAll(/['’ʼ]/g, "'")
                            );
                            console.log(`Correct answers for row ${rowIndex}, col ${colIndex}, fragment ${fragmentIndex}: ${correctAnswers}`);

                            const isCorrect = correctAnswers.includes(userAnswer);
                            console.log(`Is correct for row ${rowIndex}, col ${colIndex}, fragment ${fragmentIndex}: ${isCorrect}`);

                            this.results[rowIndex][colIndex][fragmentIndex] = isCorrect;
                        }
                    });
                });
            });

            const allCorrect = this.results.flat().every(result => result.every(res => res === true));
            console.log(`All correct: ${allCorrect}`);

            if (allCorrect) {
                this.launchConfetti();
            }
        },


        handleFocus(rowIndex, colIndex, fragmentIndex) {
            this.activeRowIndex = rowIndex;
            this.activeColIndex = colIndex;
            this.activeFragmentIndex = fragmentIndex;
        },
        handleInputChange() {
            this.clearResult();
        },
        handleDiacrtButtonClick(event) {
            this.clearResult();
            if (this.activeRowIndex === null || this.activeColIndex === null || this.activeFragmentIndex === null) {
                console.error('No active input field.');
                return;
            }
            const char = event.target.dataset.char;
            const activeElement = this.$refs[`inputField${this.activeRowIndex}-${this.activeColIndex}-${this.activeFragmentIndex}`][0];
            if (activeElement) {
                const position = activeElement.selectionStart;
                const updatedText = [
                    activeElement.value.slice(0, position),
                    char,
                    activeElement.value.slice(position),
                ].join('');
                this.userAnswers[this.activeRowIndex][this.activeColIndex][this.activeFragmentIndex] = updatedText;
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
.fill-blank-table-exercise {
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
    text-align: center;
}

.result-icon {
    top: 50%;
    transform: translateY(-50%);
    right: -1em;
}
</style>