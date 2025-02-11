<template>
    <div class="fill-blank-table-exercise">
    <table 
        class="table table-sm text-center"
        :class="data.class ? data.class : 'table-bordered'"
    >
        <tbody>
          <tr v-for="(row, rowIndex) in data.table" :key="rowIndex">
            <td v-for="(cell, colIndex) in row" :key="colIndex" :class="cell.class">
                <div class="position-relative">
                    <span v-if="!cell.content.includes('[10*:')">{{ cell.content }}</span>
                    <input 
                        v-else
                        v-model="userAnswers[rowIndex][colIndex]"
                        :ref="'inputField' + rowIndex + '-' + colIndex"
                        :style="{ 
                        width: `${getPlaceholderLength(cell.content)}em`, 
                        color: results[rowIndex][colIndex] === undefined ? 'black' : results[rowIndex][colIndex] ? 'green' : 'red' 
                        }"
                        class="form-control mx-1 input-field"
                        @input="handleInputChange"
                        @focus="handleFocus(rowIndex, colIndex)"
                        v-tooltip.right="{
                        content: getCorrectAnswers(cell.content).join(', '),
                        shown: isShowHints,
                        triggers: [],
                        delay: 0,
                        }"
                    />
                    <span v-if="results[rowIndex][colIndex] !== undefined" class="position-absolute result-icon">
                        <font-awesome-icon 
                        :icon="results[rowIndex][colIndex] ? ['fas', 'check'] : ['fas', 'xmark']" 
                        :class="results[rowIndex][colIndex] ? 'text-success' : 'text-danger'" 
                        />
                    </span>
                </div>
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
  import SpecialCharsButtons from '@/components/ui/SpecialCharsButtons.vue';
  import HintButton from '@/components/ui/HintButtonCompponent.vue';


  export default {
    name: 'FillBlankTableExerciseComponent',
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
      };
    },
    methods: {
      getPlaceholderLength(content) {
        const match = content.match(/\[(\d+)\*:/);
        return match ? Number(match[1]) + 2 : content.length;
      },
      getCorrectAnswers(content) {
        const match = content.match(/\[(\d+)\*:([^\]{]+)\]/);
        return match ? match[2].split('|') : [];
      },
      parseData() {
        this.userAnswers = this.data.table.map(row => 
          row.map(cell => (cell.content.includes('[10*:') ? '' : cell.content))
        );
        this.results = this.data.table.map(row => 
          row.map(() => undefined)
        );
      },
      clearResult() {
        this.results = this.data.table.map(row => 
          row.map(() => undefined)
        );
      },
      checkAnswers() {
        this.data.table.forEach((row, rowIndex) => {
          row.forEach((cell, colIndex) => {
            if (cell.content.includes('[10*:')) {
              const userAnswer = this.userAnswers[rowIndex][colIndex]?.toLowerCase();
              const correctAnswers = this.getCorrectAnswers(cell.content).map(ans => ans.toLowerCase());
              console.log(userAnswer, correctAnswers);
              const isCorrect = correctAnswers.includes(userAnswer);
              this.results[rowIndex][colIndex] = isCorrect;
            }
          });
        });
      },
      handleFocus(rowIndex, colIndex) {
        this.activeRowIndex = rowIndex;
        this.activeColIndex = colIndex;
      },
      handleInputChange() {
        this.clearResult();
      },
      handleDiacrtButtonClick(event) {
        this.clearResult();
        if (this.activeRowIndex === null || this.activeColIndex === null) {
          console.error('No active input field.');
          return;
        }
        const char = event.target.dataset.char;
        const activeElement = this.$refs[`inputField${this.activeRowIndex}-${this.activeColIndex}`][0];
        if (activeElement) {
          const position = activeElement.selectionStart;
          const updatedText = [
            activeElement.value.slice(0, position),
            char,
            activeElement.value.slice(position),
          ].join('');
          this.userAnswers[this.activeRowIndex][this.activeColIndex] = updatedText;
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
    right: 1em;
  }
  
  </style>
  