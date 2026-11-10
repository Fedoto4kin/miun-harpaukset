<template>
  <button
    v-if="visible"
    type="button"
    class="word-lookup-tip"
    :style="tipStyle"
    title="Löydiä šanakniigašta"
    @mousedown.prevent
    @touchstart.prevent
    @click="emitLookup"
  >
    <font-awesome-icon :icon="['fas', 'book']" />
    <span>Šanakniiga</span>
  </button>
</template>

<script>
/** Задержка после touch: iOS/Android дописывают selection после touchend. */
const TOUCH_SETTLE_MS = 120;
/** Короткий settle после mouseup / selectionchange. */
const SETTLE_MS = 30;
/** Игнор мелкого/инерционного скролла сразу после показа tip. */
const SCROLL_GRACE_MS = 400;
const SCROLL_HIDE_PX = 24;

export default {
  name: 'WordSelectionLookup',
  props: {
    /** CSS-селектор области, где ловим выделение */
    rootSelector: {
      type: String,
      default: '#lesson-frame',
    },
  },
  emits: ['lookup'],
  data() {
    return {
      visible: false,
      word: '',
      tipStyle: {},
      settleTimer: null,
      shownAt: 0,
      scrollYAtShow: 0,
    };
  },
  mounted() {
    document.addEventListener('mouseup', this.onMouseUp);
    document.addEventListener('touchend', this.onTouchEnd, { passive: true });
    document.addEventListener('selectionchange', this.onSelectionChange);
    window.addEventListener('scroll', this.onScroll, true);
    window.addEventListener('resize', this.hide);
  },
  beforeUnmount() {
    this.clearTimer();
    document.removeEventListener('mouseup', this.onMouseUp);
    document.removeEventListener('touchend', this.onTouchEnd);
    document.removeEventListener('selectionchange', this.onSelectionChange);
    window.removeEventListener('scroll', this.onScroll, true);
    window.removeEventListener('resize', this.hide);
  },
  methods: {
    clearTimer() {
      if (this.settleTimer != null) {
        clearTimeout(this.settleTimer);
        this.settleTimer = null;
      }
    },
    hide() {
      this.clearTimer();
      this.visible = false;
      this.word = '';
    },
    scheduleUpdate(delayMs) {
      this.clearTimer();
      this.settleTimer = setTimeout(() => {
        this.settleTimer = null;
        this.updateFromSelection();
      }, delayMs);
    },
    onMouseUp() {
      this.scheduleUpdate(SETTLE_MS);
    },
    onTouchEnd() {
      this.scheduleUpdate(TOUCH_SETTLE_MS);
    },
    onSelectionChange() {
      const sel = window.getSelection();
      if (!sel || sel.isCollapsed || !sel.toString().trim()) {
        // Не гасим tip сразу: на мобильных selection кратко схлопывается
        // при появлении handles / системного меню. Спрячем, если так и осталось.
        if (this.visible) {
          this.scheduleUpdate(TOUCH_SETTLE_MS);
        }
        return;
      }
      this.scheduleUpdate(SETTLE_MS);
    },
    onScroll() {
      if (!this.visible) return;
      const now = Date.now();
      if (now - this.shownAt < SCROLL_GRACE_MS) return;
      const dy = Math.abs((window.scrollY || 0) - this.scrollYAtShow);
      if (dy >= SCROLL_HIDE_PX) {
        this.hide();
      }
    },
    normalizeWord(raw) {
      const trimmed = (raw || '').replace(/\s+/g, ' ').trim();
      if (!trimmed || /\s/.test(trimmed)) return '';
      // Снять пунктуацию по краям, оставить буквы/цифры/дефис/мягкий знак.
      const cleaned = trimmed.replace(
        /^[^\p{L}\p{N}ʼ'’-]+|[^\p{L}\p{N}ʼ'’-]+$/gu,
        ''
      );
      if (!cleaned || /\s/.test(cleaned)) return '';
      return cleaned;
    },
    updateFromSelection() {
      const sel = window.getSelection();
      if (!sel || sel.rangeCount === 0 || sel.isCollapsed) {
        this.hide();
        return;
      }

      const word = this.normalizeWord(sel.toString());
      if (!word) {
        this.hide();
        return;
      }

      const node = sel.anchorNode;
      const el = node && (node.nodeType === Node.TEXT_NODE ? node.parentElement : node);
      if (!el || typeof el.closest !== 'function') {
        this.hide();
        return;
      }
      if (!el.closest(this.rootSelector)) {
        this.hide();
        return;
      }
      if (el.closest('input, textarea, .modal, .word-lookup-tip')) {
        this.hide();
        return;
      }

      const range = sel.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      if (!rect || (rect.width === 0 && rect.height === 0)) {
        this.hide();
        return;
      }

      // Держим tip в viewport по горизонтали.
      const tipHalf = 72;
      const left = Math.min(
        Math.max(rect.left + rect.width / 2, tipHalf + 8),
        window.innerWidth - tipHalf - 8
      );

      this.word = word;
      this.tipStyle = {
        top: `${Math.round(rect.bottom + 6)}px`,
        left: `${Math.round(left)}px`,
      };
      this.shownAt = Date.now();
      this.scrollYAtShow = window.scrollY || 0;
      this.visible = true;
    },
    emitLookup() {
      if (!this.word) return;
      this.$emit('lookup', this.word);
      this.hide();
      window.getSelection()?.removeAllRanges();
    },
  },
};
</script>

<style scoped>
.word-lookup-tip {
  position: fixed;
  z-index: 56000;
  transform: translateX(-50%);
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.25rem 0.55rem;
  border: 1px solid #ced4da;
  border-radius: 999px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  color: #495057;
  font-size: 0.8rem;
  line-height: 1.2;
  white-space: nowrap;
  cursor: pointer;
  /* Крупнее зона нажатия на тач */
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
}

.word-lookup-tip:hover {
  background: #f8f9fa;
  border-color: #adb5bd;
}
</style>
