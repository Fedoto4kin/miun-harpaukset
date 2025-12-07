<template>
    <div class="interactive-hint-exercise">
        <div v-for="(question, index) in data.questions" :key="index" class="hint-question mb-3">
            <div class="question-content">
                <span v-html="question.text" class="question-text"></span>
                <span  v-tooltip.left="{
                    content: question.answer,
                    shown: activeHintIndex === index,
                    triggers: [],
                    delay: 0
                }">&nbsp;</span>

                <HintButton v-if="question.hint_button !== false" class="ms-2" @pointerdown="showHint(index)"
                    @pointerup="hideHint(index)" @mouseleave="hideHint()" />
            </div>
        </div>
    </div>
</template>

<script>
import HintButton from '@/components/ui/HintButtonComponent.vue';

export default {
    name: 'InteractiveHintExerciseComponent',
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
            default: false, // Всегда false для этого типа
        },
    },
    data() {
        return {
            activeHintIndex: null,
        };
    },
    methods: {

        showHint(index) {
            this.activeHintIndex = index;
        },
        hideHint() {
              this.activeHintIndex = null;
        }
    },
};
</script>

<style scoped>
.hint-question {
    border-left: 4px solid #6c757d;
    padding-left: 15px;
}

.question-content {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
}

.question-text {
    font-size: 1.1em;
    line-height: 1.6;
}

.answer-indicator {
    display: inline-block;
    width: 20px;
    height: 20px;
    background-color: #28a745;
    color: white;
    border-radius: 50%;
    text-align: center;
    line-height: 20px;
    font-size: 0.9em;
    margin: 0 2px;
    vertical-align: middle;
}

</style>