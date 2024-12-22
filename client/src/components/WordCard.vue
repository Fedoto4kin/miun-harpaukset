<template>
  <div class="col-md-4 mb-4">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title d-flex justify-content-between align-items-center">
          <span>
            {{ word.word ? word.word.replace('|', '') : '' }}
            <span class="badge bg-secondary">{{ word.pos }}</span>
          </span>
          <button 
            @click="playSound(word.speech)" 
            :disabled="isPlaying" 
            class="btn btn-sm btn-outline-primary"
          >
            <font-awesome-icon icon="volume-up" />
          </button>
        </h5>
        <ul class="list-group list-group-flush">
          <li v-for="(def, lang) in definition(word.definition)" :key="lang" class="list-group-item">
            <div class="d-flex align-items-center">
              <img :src="'/img/' + lang + '-xs.png'" :alt="lang" class="me-2" />
              <div class="definition-content">
                <span v-if="def.length > 1">
                  <ol class="mb-0" style="margin-left: -1rem;">
                    <li v-for="d in def" :key="d">{{ d }}</li>
                  </ol>
                </span>
                <span v-else class="ms-3">{{ def[0] }}</span>
              </div>
            </div>
          </li>
        </ul>
        <div v-if="word.alias_words.length" class="mt-2">
          <span class='text-muted'>Šama kuin </span>
          <span v-for="al in alias(word.alias_words)" :key="al" class="badge bg-info me-1">{{ al }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WordCard',
  props: {
    word: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      isPlaying: false
    };
  },
  methods: {
    definition(definitions) {
      return definitions.reduce((r, a) => {
        r[a.lang] = r[a.lang] || [];
        r[a.lang].push(a.definition);
        return r;
      }, Object.create(null));
    },
    alias(aliases) {
      return aliases.map((d) => d.word.replace('|', ''));
    },
    playSound(file) {
      const audio = new Audio(file);
      this.isPlaying = true;
      audio.play();
      audio.onended = () => {
        this.isPlaying = false;
      };
    }
  }
};
</script>

<style scoped>
.card-body {
  display: flex;
  flex-direction: column;
}
.definition-content {
  margin-left: 0.5rem;
}
</style>
