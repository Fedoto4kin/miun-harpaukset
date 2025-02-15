<template>
    <ul class="list-unstyled list-group p-0">
      <li
        v-for="module in modules"
        :key="module.id"
        @click="loadModuleContent(module.id)"
        class="list-group-item d-flex align-items-center justify-content-between gap-2"
        :class="{ 'active-module': selectedModuleId === module.id }"
      >
        <span
          class="badge rounded-pill shadow-sm custom-badge"
          :class="selectedModuleId === module.id ? 'bg-primary' : 'bg-light text-muted'"
        >
          {{ module.number }}
        </span>
        <div v-if="module.tags.length > 0" class="d-flex gap-2">
          <span v-for="tag in module.tags" :key="tag.id">
            <TagIcon 
                :tagCode="tag.code" 
                :hintFinnish="tag.hint_finnish"
                :hintRussian="tag.hint_russian"
                :tagName="tag.name"
            />
          </span>
        </div>
      </li>
    </ul>
  </template>
  
  <script>
  import TagIcon from '@/components/ui/TagIcon.vue'; 
  
  export default {
    name: 'ModuleList',
    components: {
      TagIcon,
    },
    props: {
      modules: {
        type: Array,
        required: true,
      },
      selectedModuleId: {
        type: [Number, String],
        default: null,
      },
    },
    methods: {
      loadModuleContent(moduleId) {
        this.$emit('module-clicked', moduleId);
      },
    },
  };
  </script>
  
  <style scoped>
  .list-group-item {
    cursor: pointer;
    border: none;
    background-color: #f8f9fa;
    transition: background-color 0.2s ease;
  }
  
  .list-group-item:hover {
    background-color: #e9ecef;
  }
  
  .active-module {
    background-color: white !important; 
    font-weight: bold; 
  }
  
  .custom-badge {
    font-size: 0.75rem; 
    padding: 0.25rem 0.5rem; 
  }
  
  .shadow-sm {
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075); 
  }
  </style>