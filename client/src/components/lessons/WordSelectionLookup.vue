<template>
  <!-- Desktop: tip у выделения -->
  <button
    v-if="visible && !touchUi"
    type="button"
    class="word-lookup-tip"
    :style="tipStyle"
    title="Löydiä šanakniigašta"
    @mousedown.prevent
    @click="emitLookup"
  >
    <font-awesome-icon :icon="['fas', 'book']" />
    <span>Šanakniiga</span>
  </button>

  <!-- Mobile: нижняя панель — не конкурирует с системным меню выделения -->
  <div v-if="visible && touchUi" class="word-lookup-bar" role="dialog" aria-label="Šanakniiga">
    <div class="word-lookup-bar__main">
      <span class="word-lookup-bar__word">{{ word }}</span>
      <button type="button" class="word-lookup-bar__action" @click="emitLookup">
        <font-awesome-icon :icon="['fas', 'book']" />
        <span>Šanakniiga</span>
      </button>
    </div>
    <button
      type="button"
      class="word-lookup-bar__close"
      aria-label="Sulgie"
      @click="hide"
    >
      ×
    </button>
  </div>
</template>

<script>
const TOUCH_MQ = '(pointer: coarse)';
const SETTLE_MS = 30;
const SCROLL_GRACE_MS = 400;
const SCROLL_HIDE_PX = 24;
const TAP_MOVE_PX = 12;
const TAP_MAX_MS = 450;
const WORD_CHAR = /[\p{L}\p{N}ʼ'’-]/u;

const SKIP_CLOSEST =
  'a, button, input, textarea, select, .modal, .exercise-container, .word-lookup-tip, .word-lookup-bar, .sticky-lesson';

export default {
  name: 'WordSelectionLookup',
  props: {
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
      touchUi: false,
      settleTimer: null,
      shownAt: 0,
      scrollYAtShow: 0,
      mediaQuery: null,
      tapStart: null,
    };
  },
  mounted() {
    this.mediaQuery = window.matchMedia(TOUCH_MQ);
    this.touchUi = this.mediaQuery.matches;
    if (this.mediaQuery.addEventListener) {
      this.mediaQuery.addEventListener('change', this.onTouchUiChange);
    } else {
      this.mediaQuery.addListener(this.onTouchUiChange);
    }
    this.bindModeListeners(true);
    window.addEventListener('scroll', this.onScroll, true);
    window.addEventListener('resize', this.hide);
  },
  beforeUnmount() {
    this.clearTimer();
    this.bindModeListeners(false);
    if (this.mediaQuery) {
      if (this.mediaQuery.removeEventListener) {
        this.mediaQuery.removeEventListener('change', this.onTouchUiChange);
      } else {
        this.mediaQuery.removeListener(this.onTouchUiChange);
      }
    }
    window.removeEventListener('scroll', this.onScroll, true);
    window.removeEventListener('resize', this.hide);
  },
  methods: {
    onTouchUiChange(event) {
      this.bindModeListeners(false);
      this.touchUi = event.matches;
      this.hide();
      this.bindModeListeners(true);
    },
    bindModeListeners(on) {
      const fn = on ? 'addEventListener' : 'removeEventListener';
      if (this.touchUi) {
        document[fn]('touchstart', this.onTapStart, { passive: true });
        document[fn]('touchend', this.onTapEnd, { passive: true });
        document[fn]('selectionchange', this.onMobileSelectionChange);
      } else {
        document[fn]('mouseup', this.onMouseUp);
        document[fn]('selectionchange', this.onDesktopSelectionChange);
      }
    },
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
    schedule(fn, delayMs) {
      this.clearTimer();
      this.settleTimer = setTimeout(() => {
        this.settleTimer = null;
        fn();
      }, delayMs);
    },
    onMouseUp() {
      this.schedule(() => this.updateFromSelection(false), SETTLE_MS);
    },
    onDesktopSelectionChange() {
      const sel = window.getSelection();
      if (!sel || sel.isCollapsed || !sel.toString().trim()) {
        if (this.visible) this.hide();
        return;
      }
      this.schedule(() => this.updateFromSelection(false), SETTLE_MS);
    },
    onMobileSelectionChange() {
      // Длинное выделение: подтянуть слово в нижнюю панель (под системным меню).
      const sel = window.getSelection();
      if (!sel || sel.isCollapsed || !sel.toString().trim()) return;
      this.schedule(() => this.updateFromSelection(true), 80);
    },
    onTapStart(event) {
      const t = event.changedTouches?.[0] || event.touches?.[0];
      if (!t) return;
      this.tapStart = {
        x: t.clientX,
        y: t.clientY,
        at: Date.now(),
      };
    },
    onTapEnd(event) {
      const start = this.tapStart;
      this.tapStart = null;
      if (!start) return;
      const t = event.changedTouches?.[0];
      if (!t) return;
      const dt = Date.now() - start.at;
      const dx = Math.abs(t.clientX - start.x);
      const dy = Math.abs(t.clientY - start.y);
      if (dt > TAP_MAX_MS || dx > TAP_MOVE_PX || dy > TAP_MOVE_PX) return;

      // Если уже есть выделение — пусть selectionchange обработает.
      const sel = window.getSelection();
      if (sel && !sel.isCollapsed && sel.toString().trim()) return;

      const hit = this.wordAtPoint(t.clientX, t.clientY);
      if (!hit) return;
      this.showWord(hit.word, hit.rect, true);
    },
    onScroll() {
      if (!this.visible || this.touchUi) return;
      if (Date.now() - this.shownAt < SCROLL_GRACE_MS) return;
      const dy = Math.abs((window.scrollY || 0) - this.scrollYAtShow);
      if (dy >= SCROLL_HIDE_PX) this.hide();
    },
    normalizeWord(raw) {
      const trimmed = (raw || '').replace(/\s+/g, ' ').trim();
      if (!trimmed || /\s/.test(trimmed)) return '';
      const cleaned = trimmed.replace(
        /^[^\p{L}\p{N}ʼ'’-]+|[^\p{L}\p{N}ʼ'’-]+$/gu,
        ''
      );
      if (!cleaned || /\s/.test(cleaned)) return '';
      return cleaned;
    },
    isAllowedElement(el) {
      if (!el || typeof el.closest !== 'function') return false;
      if (!el.closest(this.rootSelector)) return false;
      if (el.closest(SKIP_CLOSEST)) return false;
      return true;
    },
    wordAtPoint(x, y) {
      let node = null;
      let offset = 0;
      if (document.caretRangeFromPoint) {
        const range = document.caretRangeFromPoint(x, y);
        if (!range) return null;
        node = range.startContainer;
        offset = range.startOffset;
      } else if (document.caretPositionFromPoint) {
        const pos = document.caretPositionFromPoint(x, y);
        if (!pos) return null;
        node = pos.offsetNode;
        offset = pos.offset;
      } else {
        return null;
      }
      if (!node || node.nodeType !== Node.TEXT_NODE) return null;
      const parent = node.parentElement;
      if (!this.isAllowedElement(parent)) return null;

      const text = node.textContent || '';
      if (!text || offset < 0 || offset > text.length) return null;
      let i = Math.min(offset, text.length - 1);
      if (i < 0) return null;
      if (!WORD_CHAR.test(text[i])) {
        if (i > 0 && WORD_CHAR.test(text[i - 1])) i -= 1;
        else return null;
      }
      let start = i;
      let end = i + 1;
      while (start > 0 && WORD_CHAR.test(text[start - 1])) start -= 1;
      while (end < text.length && WORD_CHAR.test(text[end])) end += 1;
      const word = this.normalizeWord(text.slice(start, end));
      if (!word) return null;

      const range = document.createRange();
      range.setStart(node, start);
      range.setEnd(node, end);
      const rect = range.getBoundingClientRect();
      return { word, rect };
    },
    updateFromSelection(preferBar) {
      const sel = window.getSelection();
      if (!sel || sel.rangeCount === 0 || sel.isCollapsed) {
        if (!preferBar) this.hide();
        return;
      }
      const word = this.normalizeWord(sel.toString());
      if (!word) {
        if (!preferBar) this.hide();
        return;
      }
      const node = sel.anchorNode;
      const el = node && (node.nodeType === Node.TEXT_NODE ? node.parentElement : node);
      if (!this.isAllowedElement(el)) {
        if (!preferBar) this.hide();
        return;
      }
      const range = sel.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      if (!rect || (rect.width === 0 && rect.height === 0)) {
        if (!preferBar) this.hide();
        return;
      }
      this.showWord(word, rect, preferBar || this.touchUi);
    },
    showWord(word, rect, asBar) {
      this.word = word;
      this.shownAt = Date.now();
      this.scrollYAtShow = window.scrollY || 0;

      if (asBar || this.touchUi) {
        this.tipStyle = {};
        this.visible = true;
        return;
      }

      const tipHalf = 72;
      const left = Math.min(
        Math.max(rect.left + rect.width / 2, tipHalf + 8),
        window.innerWidth - tipHalf - 8
      );
      this.tipStyle = {
        top: `${Math.round(rect.bottom + 6)}px`,
        left: `${Math.round(left)}px`,
      };
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
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
}

.word-lookup-tip:hover {
  background: #f8f9fa;
  border-color: #adb5bd;
}

.word-lookup-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 56000;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 0.75rem calc(0.65rem + env(safe-area-inset-bottom, 0px));
  background: #fff;
  border-top: 1px solid #dee2e6;
  box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.12);
}

.word-lookup-bar__main {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.65rem;
  min-width: 0;
}

.word-lookup-bar__word {
  font-weight: 600;
  font-size: 1.05rem;
  color: #212529;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.word-lookup-bar__action {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  flex-shrink: 0;
  padding: 0.45rem 0.8rem;
  border: none;
  border-radius: 999px;
  background: #0d6efd;
  color: #fff;
  font-size: 0.9rem;
  line-height: 1.2;
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
}

.word-lookup-bar__action:active {
  background: #0b5ed7;
}

.word-lookup-bar__close {
  flex-shrink: 0;
  width: 2rem;
  height: 2rem;
  border: none;
  border-radius: 50%;
  background: #f1f3f5;
  color: #495057;
  font-size: 1.35rem;
  line-height: 1;
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
}
</style>
