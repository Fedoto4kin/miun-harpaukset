<template>
  <button
    v-if="visible"
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
</template>

<script>
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
    };
  },
  mounted() {
    document.addEventListener('mouseup', this.onPointerUp);
    document.addEventListener('touchend', this.onPointerUp, { passive: true });
    document.addEventListener('selectionchange', this.onSelectionChange);
    window.addEventListener('scroll', this.hide, true);
    window.addEventListener('resize', this.hide);
  },
  beforeUnmount() {
    document.removeEventListener('mouseup', this.onPointerUp);
    document.removeEventListener('touchend', this.onPointerUp);
    document.removeEventListener('selectionchange', this.onSelectionChange);
    window.removeEventListener('scroll', this.hide, true);
    window.removeEventListener('resize', this.hide);
  },
  methods: {
    hide() {
      this.visible = false;
      this.word = '';
    },
    onSelectionChange() {
      const sel = window.getSelection();
      if (!sel || sel.isCollapsed || !sel.toString().trim()) {
        this.hide();
      }
    },
    onPointerUp() {
      // Дать браузеру зафиксировать selection (особенно touch).
      setTimeout(() => this.updateFromSelection(), 10);
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

      this.word = word;
      this.tipStyle = {
        top: `${Math.round(rect.bottom + 6)}px`,
        left: `${Math.round(rect.left + rect.width / 2)}px`,
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
}

.word-lookup-tip:hover {
  background: #f8f9fa;
  border-color: #adb5bd;
}
</style>
