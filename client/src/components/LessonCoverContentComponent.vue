<template>
    <div class="widget-content">
        <div class="border-bottom">
            <h3 class="display-6 text-center">{{ lesson.full_name }}</h3>
        </div>
        <div>
            <blockquote class="blockquote text-center">
                <h4 class="display-5 lead">{{ lesson.slogan }}</h4>
            </blockquote>
        </div>
        <div class="card lesson-description text-center mb-3">
            <div class="card-header">
                {{ lesson.description }}
            </div>
        </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LessonCoverContent',
    props: {
      lesson: {
        type: Object,
        required: true,
      },
    },
  };
  </script>
  
  <style scoped>
  .widget-content {
    padding: 20px;
  }
  
  .widget-content audio {
    margin-top: 10px;
    width: 100%;
  }
  
  .widget-content p {
    margin-top: 15px;
    font-size: 16px;
  }

  .lesson-description {
    font-size: 1.25em;;
    border-left: 0.5rem solid rgba(0, 123, 255, 0.54);
  }
  </style>
  