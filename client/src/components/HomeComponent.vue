<template>
    <div class="container">
      <div class="row">
        <div class="col-md-4 align-items-center">
            <img src="/img/book.jpg" class="my-5 w-100" />
        </div>
        <div class="col-md-6">
          <div class="row">
            <div class="row mt-5">
              <audio controls>
                <source src="/media/intro.mp3" type="audio/mpeg">
                Your browser does not support the audio tag.
              </audio>
              <h3 class="ps-4 mt-3">Miun harpaukšet karielan kieleh</h3>
              <h4 class="ps-4">Tverinkarielan algukursa</h4>
            </div>
          </div>
          <div class="row mt-3">
            <div class="col-md-12">
              <h5 class="ps-4 mb-3">Hyvä tverinkarielan opaštuja!</h5>
              <p class="justify-content-between" style="text-indent: 1.5em;">
                Šiun käzissä on Miun harpaukšet karielan kieleh -kniiga, kumbazen avulla voit opaštuo tädä šomua tverinkerielan kieldä.
                Tverinkarielakši paissah karielazet, kumbazet jo enämbi nelliä vuožišadua eletäh Tverin mualla. Voit olla tämä pagina ei ole
                vieraš šiula varoin. Paissahgo karielakši šiun vanhemmat? Paistihgo buabot da diedot? Maltatgo iče karielua ali tahot opaštuo
                maltamah da pagizomah?
            </p>
                <p style="text-indent: 1.5em;">Tverinkarielan algukursa auttau šiula luadie enžimäzet harpaukšet karielan kieleh. Kniigašša on
                <a href="/lessons/">25 urokkua</a>. Jogohizešta löyvät uužie šanoida, grammatikkua, annandoida da kaikenmuozie tekstoida. 
                Štobi šiula olisʼ kebiembi
                opaštuo pagizomah oigieh, myö kirjuttima DVD-diskan, kumbazešta voiččou kuunnella kuin pagizou tovelline karielane.
                Tämä kniiga on yksikieline, ka šiula avukši ollah veniälänkielizet kommentarijat, avuamet, 
                grammatičeskoit tabličat da <a href="/lexicon/">kariela–veniälä–šuomi šanakniiga</a>.
                </p>
                <p style="text-indent: 1.5em;">Hyviä opaššundua šiula! Rubiemma pagizomah karielakši!</p>
                <p class="text-end">Tervehyzin, kakši Iruo,<br> Šalon da Puasinkoin</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomeComponent',
    mounted() {
      document.title = 'Miun harpaukšet Karielan Kieleh';
    }
  };
  </script>
  
  <style scoped>

  .justify-content-between {
    text-indent: 1.5em;
  }
  </style>
  