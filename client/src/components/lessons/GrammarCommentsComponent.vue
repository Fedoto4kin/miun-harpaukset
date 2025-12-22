<template>
  <div v-if="comment && comment.html_content" class="grammar-comments-container mt-4">
    <div class="card border-0">
      <div class="card-header bg-light border-0 py-2">
        <button 
          class="btn btn-link p-0 text-decoration-none w-100 text-start"
          type="button"
          data-bs-toggle="collapse"
          :data-bs-target="'#grammarCard' + comment.id"
          aria-expanded="false"
          :aria-controls="'grammarCard' + comment.id"
        >
          <div class="d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center">
              <font-awesome-icon :icon="['fas', 'info-circle']" class="text-info me-1" />
              <img :src="'/img/ru-md.png'" class="ms-1" style="height: 24px;" />
              <span class="ms-2 fw-semibold text-dark"></span>
            </div>
            <div class="collapse-indicator">
              <font-awesome-icon 
                :icon="['fas', 'chevron-down']" 
                class="ms-2"
                :class="{ 'rotated': isOpen }"
              />
            </div>
          </div>
        </button>
      </div>
      <div 
        :id="'grammarCard' + comment.id" 
        class="collapse"
        data-bs-parent=".grammar-comments-container"
      >
        <div class="card-body bg-light p-0">
          <div class="grammar-comment-card">
            <div class="comment-content" v-html="comment.html_content"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GrammarCommentsComponent',
  props: {
    comment: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      isOpen: false
    };
  },
  mounted() {
    // Слушаем события collapse для обновления иконки
    const collapseElement = document.getElementById('grammarCard' + this.comment.id);
    if (collapseElement) {
      collapseElement.addEventListener('show.bs.collapse', () => {
        this.isOpen = true;
      });
      collapseElement.addEventListener('hide.bs.collapse', () => {
        this.isOpen = false;
      });
    }
  }
}
</script>

<style scoped>
.grammar-comments-container {
  border-top: 2px dashed #e9ecef;
  padding-top: 1.5rem;
}

.card {
  background-color: transparent;
}

.card-header {
  background-color: #f8f9fa !important;
  border-radius: 8px 8px 0 0;
  cursor: pointer;
  border: none;
}

.card-header:hover {
  background-color: #f0f3f5 !important;
}

.collapse-indicator {
  transition: all 0.3s ease;
  color: #6c757d;
}

.collapse-indicator .rotated {
  transform: rotate(180deg);
}

.grammar-comment-card {
  background-color: #f8f9fa;
  border-radius: 0 0 8px 8px;
  padding: 1.5rem;
  border: 1px solid #e9ecef;
  border-top: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.comment-content {
  line-height: 1.6;
  color: #212529;
}

.comment-content >>> h1,
.comment-content >>> h2,
.comment-content >>> h3,
.comment-content >>> h4 {
  color: #2c3e50;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
}

.comment-content >>> ul,
.comment-content >>> ol {
  margin-left: 1.5rem;
  margin-bottom: 1rem;
}

.comment-content >>> li {
  margin-bottom: 0.5rem;
}

.comment-content >>> table {
  width: 100%;
  margin-bottom: 1rem;
  border-collapse: collapse;
  background-color: white;
}

.comment-content >>> table th {
  background-color: #f1f3f4;
  font-weight: 600;
}

.comment-content >>> table th,
.comment-content >>> table td {
  padding: 0.75rem;
  border: 1px solid #dee2e6;
  text-align: left;
}

.comment-content >>> blockquote {
  border-left: 4px solid #3498db;
  padding-left: 1rem;
  margin-left: 0;
  margin-right: 0;
  font-style: italic;
  color: #6c757d;
  background-color: #f1f3f4;
  padding: 1rem;
  border-radius: 0 4px 4px 0;
}

.comment-content >>> code {
  background-color: #f1f3f4;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
}

@media (max-width: 768px) {
  .grammar-comments-container {
    padding-top: 1rem;
  }
  
  .grammar-comment-card {
    padding: 1rem;
  }
  
  .card-header {
    padding: 0.75rem;
  }
}
</style>