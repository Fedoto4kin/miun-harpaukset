<template>
    <div class="container-404">
      <div class="row text-center pt-5">
        <div>
          <h4>A-voi-voi</h4>
          <h1>404 - Ei ole lehtie</h1>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NotFoundComponent',
  };
  </script>
  
  <style>
  /* Стили для компонента */
  .container-404 {
    background-image: url('@/assets/img/pieni-musta-kazi.png');
    background-size: cover;
    background-position: top;
    min-height: 100vh;
    background-size: 50% auto;
    background-repeat: no-repeat;
    position: relative;
    overflow: hidden;
  }
  .container-404 .row {
    background: rgba(255, 255, 255, 0.8);
    padding: 20px;
    z-index: 10;
    position: relative;
  }
  </style>
  