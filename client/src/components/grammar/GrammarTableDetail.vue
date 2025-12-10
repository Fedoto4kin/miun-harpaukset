<template>
  <div class="container-lg py-4">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status">
      </div>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    
    <div v-else-if="table">
      <div class="h2 text-center fw-bold">{{ table.title }}</div>
      <div class="grammar-content p-4" v-html="table.html_content"></div>
    </div>
  </div>
</template>

<script>
import { grammarService } from '@/services/grammarService'

export default {
  name: 'GrammarTableDetail',
  props: ['id'],
  data() {
    return {
      table: null,
      loading: false,
      error: null
    }
  },
  created() {
    this.fetchTable()
  },
  watch: {
    id() {
      this.fetchTable()
    }
  },
  methods: {
    async fetchTable() {
      if (!this.id) return
      
      this.loading = true
      this.error = null
      this.isNotFoundError = false
      
      try {
        const response = await grammarService.getById(this.id)
        this.table = response.data
        document.title = 'Grammatikka | ' + this.table.title
      } catch (err) {
        if (err.response && err.response.status === 404) {
          this.isNotFoundError = true
          this.$router.push({ name: 'NotFound' })
        } else {
          this.error = 'Error';
          console.error(err);
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.grammar-content {
  background: #fff;
  overflow-x: auto;
  padding: 1rem;
}

.grammar-content >>> table {
  border-collapse: collapse;
  margin: 0 auto;
  min-width: 600px;
}

.grammar-content >>> table {
  border-collapse: collapse;
  margin: 0 auto;
  max-width: 1200px; /* Максимальная ширина таблицы */
  width: 100%; /* Растягивается до max-width */
}
</style>