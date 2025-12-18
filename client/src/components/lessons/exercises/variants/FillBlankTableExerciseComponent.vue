<template>
    <div class="fill-blank-table-exercise table-responsive mt-2">
        <table class="table table-sm align-bottom mb-5" :class="data.class ? data.class : 'table-bordered'">
            <tbody>
                <tr v-for="(row, rowIndex) in data.table" :key="rowIndex">
                    <td v-for="(cell, colIndex) in row" :key="colIndex" :class="cell.class">
                        <template v-for="(fragment, fragmentIndex) in parseContent(cell.content)" :key="fragmentIndex">
                            <span v-if="fragment.type === 'text'" v-html="fragment.value" />
                            <span v-else-if="fragment.type === 'span'" class="form-control mx-1 input-field text-wrap"
                                :style="{ width: `${calculateExampleStringField(fragment.value ?? '')}em` }"
                                v-html="fragment.value ?? '&nbsp;'" />
                            <span v-else class="position-relative input-wrapper">
                                <input v-model="userAnswers[rowIndex][colIndex][fragmentIndex]"
                                    :ref="'inputField' + rowIndex + '-' + colIndex + '-' + fragmentIndex" :style="{
                                        width: `${fragment.placeholderLength}em`,
                                        color: results[rowIndex][colIndex][fragmentIndex] === undefined ? 'black' : results[rowIndex][colIndex][fragmentIndex] ? 'green' : 'red'
                                    }" class="form-control mx-1 input-field" 
                                    @input="handleInputChange"
                                    @focus="handleFocus(rowIndex, colIndex, fragmentIndex)"
                                    @blur="handleBlur(rowIndex, colIndex, fragmentIndex)" />

                                <!-- Подсказка поверх поля ввода -->
                                <div v-if="isShowHints && hintForField[rowIndex]?.[colIndex]?.[fragmentIndex]"
                                    class="hint-overlay"
                                    :style="{ width: `${fragment.placeholderLength * 1.1}em` }">
                                    {{ fragment.correctAnswers.join(' | ') }}
                                </div>

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
            hintForField: [],
            focusedFields: [] // Отслеживаем фокус на полях
        };
    },
    methods: {
        calculateExampleStringField(exampleString) {
            return exampleString.replace(/<\/?[^>]+(>|$)/g, "").length * 0.7;
        },
        
        parseContent(content) {
            if (!content) {
                return [];
            }

            const fragments = [];
            let remainingContent = content;
            
            // Обновляем регулярное выражение для поддержки {PREFILLED} после ANSWERS
            const regex = /\[(\d+)\*:([^\]{]+)({[^}]+})?\]|\{([^}]+)\}/g;
            let match;

            while ((match = regex.exec(remainingContent)) !== null) {
                const textBefore = remainingContent.slice(0, match.index);
                if (textBefore.length > 0) {
                    fragments.push({ type: 'text', value: textBefore });
                }

                if (match[1]) { // Обработка разметки [n*:ANSWERS{PREFILLED}]
                    const prefilledValue = match[3] ? match[3].slice(1, -1) : '';
                    fragments.push({ 
                        type: 'blank', 
                        id: match[1],
                        placeholderLength: Number(match[1]) + 2,
                        correctAnswers: match[2].split('|'),
                        prefilledValue: prefilledValue,
                        value: match[0] // Сохраняем оригинальную строку для обратной совместимости
                    });
                } else if (match[4]) { // Обработка разметки {TEXT}
                    fragments.push({ type: 'span', value: match[4] });
                }

                remainingContent = remainingContent.slice(match.index + match[0].length);
            }

            if (remainingContent.length > 0) {
                fragments.push({ type: 'text', value: remainingContent });
            }

            return fragments;
        },

        getCorrectAnswers(content) {
            // Для обратной совместимости со старым форматом без prefilled
            const match = content.match(/\[(\d+)\*:([^\]{]+)\]/);
            if (match) {
                return match[2].split('|');
            }
            return [];
        },

        parseData() {
            this.userAnswers = this.data.table.map(row =>
                row.map(cell => {
                    const fragments = this.parseContent(cell.content);
                    return fragments.map(fragment => {
                        if (fragment.type === 'blank') {
                            // Используем предзаполненное значение, если оно есть
                            return fragment.prefilledValue || '';
                        } else if (fragment.type === 'span') {
                            return fragment.value;
                        } else {
                            return '';
                        }
                    });
                })
            );
            
            this.results = this.data.table.map(row =>
                row.map(cell => {
                    const fragments = this.parseContent(cell.content);
                    return fragments.map(() => undefined);
                })
            );
            
            this.hintForField = this.data.table.map(row =>
                row.map(cell => {
                    const fragments = this.parseContent(cell.content);
                    return fragments.map(() => false);
                })
            );
            
            this.focusedFields = this.data.table.map(row =>
                row.map(cell => {
                    const fragments = this.parseContent(cell.content);
                    return fragments.map(() => false);
                })
            );
        },

        clearResult() {
            this.results = this.data.table.map(row =>
                row.map(cell => {
                    const fragments = this.parseContent(cell.content);
                    return fragments.map(() => undefined);
                })
            );
        },

        toggleShowHints(show) {
            this.isShowHints = show;
            document.querySelectorAll('.input-field').forEach(input => {
                input.blur();
            });

            if (show) {
                this.hintForField = this.data.table.map(row =>
                    row.map(cell => {
                        const fragments = this.parseContent(cell.content);
                        return fragments.map(fragment =>
                            fragment.type === 'blank'
                        );
                    })
                );
            } else {
                this.hintForField = this.data.table.map(() =>
                    this.data.table[0].map(() => [])
                );
            }
        },

        checkAnswers() {
            this.clearResult();
            let allCorrect = true;
            
            this.data.table.forEach((row, rowIndex) => {
                row.forEach((cell, colIndex) => {
                    const fragments = this.parseContent(cell.content);
                    fragments.forEach((fragment, fragmentIndex) => {
                        if (fragment.type === 'blank') {
                            const userAnswer = this.userAnswers[rowIndex][colIndex][fragmentIndex]
                                ?.toLowerCase()
                                .replaceAll(/['’ʼ]/g, "'");

                            const correctAnswers = fragment.correctAnswers.map(ans =>
                                ans.toLowerCase().replaceAll(/['’ʼ]/g, "'")
                            );

                            const isCorrect = correctAnswers.includes(userAnswer);
                            this.results[rowIndex][colIndex][fragmentIndex] = isCorrect;
                            
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

        handleFocus(rowIndex, colIndex, fragmentIndex) {
            this.activeRowIndex = rowIndex;
            this.activeColIndex = colIndex;
            this.activeFragmentIndex = fragmentIndex;

            // Помечаем поле как сфокусированное
            if (!this.focusedFields[rowIndex]) {
                this.focusedFields[rowIndex] = [];
            }
            if (!this.focusedFields[rowIndex][colIndex]) {
                this.focusedFields[rowIndex][colIndex] = [];
            }
            this.focusedFields[rowIndex][colIndex][fragmentIndex] = true;

            // Показываем подсказку для этого поля, если включены подсказки
            if (this.isShowHints) {
                if (!this.hintForField[rowIndex]) {
                    this.hintForField[rowIndex] = [];
                }
                if (!this.hintForField[rowIndex][colIndex]) {
                    this.hintForField[rowIndex][colIndex] = [];
                }
                this.hintForField[rowIndex][colIndex][fragmentIndex] = true;
            }
        },

        handleBlur(rowIndex, colIndex, fragmentIndex) {
            // Убираем фокус
            if (this.focusedFields[rowIndex] && this.focusedFields[rowIndex][colIndex]) {
                this.focusedFields[rowIndex][colIndex][fragmentIndex] = false;
            }

            // Убираем подсказку при потере фокуса, если подсказки включены
            if (this.isShowHints) {
                if (this.hintForField[rowIndex] && this.hintForField[rowIndex][colIndex]) {
                    this.hintForField[rowIndex][colIndex][fragmentIndex] = false;
                }
            }
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
    font-size: 1.1em;
}

.fill-blank-table-exercise table {
    min-width: 800px;
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
    position: relative;
    z-index: 1;
}

.result-icon {
    top: 50%;
    transform: translateY(-50%);
    right: -2px;
    z-index: 3;
}
</style>