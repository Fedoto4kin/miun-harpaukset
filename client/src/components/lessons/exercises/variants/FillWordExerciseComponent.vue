<template>
    <div id="scene" @mouseleave="onMouseUp">
        <div class="row">
            <div class="col-8">
                <div class="field">
                    <div v-for="(row, rowIndex) in scene" :key="rowIndex" class="field-row">
                        <div class="cell"
                            :class="{ active: cell.active, hover: isHovered(rowIndex, cellIndex), prefilled: cell.prefilled }"
                            :data-row="rowIndex" :data-cell="cellIndex" 
                            @mouseover="onMouseOver"
                            @mouseenter="onMouseEnter" 
                            @mouseleave="onMouseLeave" 
                            @mousedown="onMouseDown"
                            @mouseup="onMouseUp"
                            @touchstart="onTouchStart"
                            @touchmove="onTouchMove"
                            @touchend="onTouchEnd"
                            v-for="(cell, cellIndex) in row" :key="cellIndex">
                            {{ cell.char }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-4">
                <div class="found-words align-items-center d-flex gap-2">
                    <span class="found-word btn btn-outline-secondary btn-lg hover no-pointer" 
                          v-for="(word, index) in found" :key="index">
                       {{ word }}
                    </span>
                </div>
            </div> 
        </div>
    </div>
</template>

<script>
import { confettiMixin } from '@/mixins/confettiMixin.js';

export default {
    name: 'FillWord',
    mixins: [confettiMixin],
    props: {
        data: {
            type: Object,
            required: true,
            validator(value) {
                return value && Array.isArray(value.field) && Array.isArray(value.words);
            }
        }
    },
    data() {
        return {
            scene: [],
            words: [],
            prefilledWords: [],
            found: [],
            line: [],
            word: [],
            draw: false,
            hoveredCell: null,
            isTouching: false // Флаг для отслеживания касания
        };
    },
    computed: {
        foundCount() {
            return this.found.length;
        }
    },
    watch: {
        data: {
            immediate: true,
            handler(newData) {
                if (newData) {
                    this.newGame();
                }
            }
        }
    },
    methods: {
        // Обработка событий мыши
        onMouseEnter({ target }) {
            let row = +target.dataset.row;
            let cell = +target.dataset.cell;
            this.hoveredCell = { row, cell };
        },
        onMouseLeave() {
            this.hoveredCell = null;
        },
        onMouseDown({ target }) {
            if (target.classList.contains('prefilled')) return;

            this.draw = true;
            let row = +target.dataset.row;
            let cell = +target.dataset.cell;

            if (this.isActive(row, cell)) return;

            this.activate(row, cell);
            this.$forceUpdate();
        },
        onMouseUp() {
            this.draw = false;
            this.checkWord();
        },
        onMouseOver({ target }) {
            if (!this.draw || target.classList.contains('prefilled')) return;

            let row = +target.dataset.row;
            let cell = +target.dataset.cell;

            if (!this.isActive(row, cell) && this.lastCellLengthEqualOneCell(row, cell)) {
                this.activate(row, cell);
            } else if (this.isPrevCell(row, cell)) {
                this.deactivate(this.lastCell().row, this.lastCell().cell);
                this.removeLastMoveInTimeline();
            }

            this.$forceUpdate();
        },

        // Обработка сенсорных событий
        onTouchStart(event) {
            event.preventDefault(); // Предотвращаем стандартное поведение
            this.isTouching = true;

            const touch = event.touches[0];
            const target = document.elementFromPoint(touch.clientX, touch.clientY);

            if (target && target.classList.contains('cell')) {
                this.onMouseDown({ target });
            }
        },
        onTouchMove(event) {
            if (!this.isTouching) return;

            const touch = event.touches[0];
            const target = document.elementFromPoint(touch.clientX, touch.clientY);

            if (target && target.classList.contains('cell')) {
                this.onMouseOver({ target });
            }
        },
        onTouchEnd() {
            this.isTouching = false;
            this.onMouseUp();
        },

        // Общие методы
        isHovered(row, cell) {
            return this.hoveredCell && this.hoveredCell.row === row && this.hoveredCell.cell === cell;
        },
        isActive(row, cell) {
            return this.scene[row] && this.scene[row][cell] && this.scene[row][cell].active;
        },
        activate(row, cell) {
            if (this.scene[row] && this.scene[row][cell]) {
                this.scene[row][cell].active = true;
                this.addTimeline(row, cell);
                this.addChar(this.scene[row][cell].char);
            }
        },
        deactivate(row, cell) {
            if (this.scene[row] && this.scene[row][cell]) {
                this.scene[row][cell].active = false;
                this.removeLastChar();
            }
        },
        deactivateTimeline() {
            this.line.forEach(item => {
                if (this.scene[item.row] && this.scene[item.row][item.cell]) {
                    this.scene[item.row][item.cell].active = false;
                }
            });

            this.line = [];
        },
        addTimeline(row, cell) {
            this.line.push({ row, cell });
        },
        removeLastMoveInTimeline() {
            this.line.splice(this.line.length - 1, 1);
        },
        prevCell() {
            return this.line[this.line.length - 2];
        },
        lastCell() {
            return this.line[this.line.length - 1];
        },
        isPrevCell(row, cell) {
            if (!this.prevCell()) return false;

            return this.prevCell().row === row && this.prevCell().cell === cell;
        },
        lastCellLengthEqualOneCell(row, cell) {
            let lastRow = this.lastCell().row;
            let lastCell = this.lastCell().cell;

            return (
                ((lastRow === row - 1 || lastRow === row + 1) && lastCell === cell) ||
                ((lastCell === cell - 1 || lastCell === cell + 1) && lastRow === row)
            );
        },
        addChar(char) {
            this.word.push(char);
        },
        removeLastChar() {
            this.word.splice(this.word.length - 1, 1);
        },
        clearWord() {
            this.word = [];
        },
        checkWord() {
            let word = this.hasWord();

            if (word) {
                this.line = [];
                const foundWord = this.word.join("").toLowerCase();
                this.found.unshift(foundWord);
                this.words = this.words.filter(w => w.toLowerCase() !== foundWord);
                
                this.clearWord();

                if (this.isEndGame()) {
                    this.launchConfetti();
                }
            } else {
                this.deactivateTimeline();
            }

            this.clearWord();
            this.$forceUpdate();
        },
        hasWord() {
            return this.words.filter(word => {
                return this.word.join("") === word.toUpperCase();
            })[0];
        },
        isEndGame() {
            return this.words.length === 0;
        },
        makeEmptyScene() {
            this.scene = [];
            for (let row = 0; row < 11; row++) {
                let line = [];

                for (let cell = 0; cell < 11; cell++) {
                    line.push({ char: null, active: false, prefilled: false });
                }

                this.scene.push(line);
            }
        },
        markPrefilledCells() {
            if (this.data.prefilledWords) {
                this.found = []; 

                Object.entries(this.data.prefilledWords).forEach(([word, coordinates]) => {
                    if (!this.found.includes(word)) {
                        this.found.push(word);
                    }
                    coordinates.forEach(coord => {
                        const [x, y] = coord.split(':').map(Number);
                        const row = x - 1; // Нумерация с 0
                        const cell = y - 1; // Нумерация с 0

                        if (this.scene[row] && this.scene[row][cell]) {
                            this.scene[row][cell].active = true; // Закрашиваем ячейку
                            this.scene[row][cell].prefilled = true; // Помечаем как предзаполненную
                        }
                    });
                });
            }
        },
        newGame() {
            if (this.data && this.data.words && this.data.field) {
                this.words = this.data.words;
                this.prefilledWords = this.data.prefilledWords || [];
                this.scene = this.data.field.map(row => row.split('').map(char => ({ char: char.toUpperCase(), active: false, prefilled: false })));

                this.markPrefilledCells();
            } else {
                console.error("Data is not available or has incorrect structure");
            }
        }
    },
    created() {
        this.makeEmptyScene();
        if (this.data) {
            this.newGame();
        }
    }
};
</script>

<style scoped>
#scene {
    display: grid;
    gap: 0;
}

.container {
    display: flex;
    align-items: flex-start;
}

.field-row {
    display: grid;
    user-select: none;
    min-width: 75%;
}

.field-row {
    display: grid;
    grid-template-columns: repeat(11, 40px);
    padding-left: 1em;
}

.cell {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border: 1px solid #000;
    text-align: center;
    font-size: 1.5em;
    cursor: pointer;
}

.cell.hover {
    background-color: #abebff;
}

.cell.active {
    background-color: #d4edda;
}

.cell.prefilled {
    background-color: #d3d3d3;
    pointer-events: none;
}

.no-pointer {
    pointer-events: none;
}

.found-words {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}
</style>