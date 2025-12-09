<template>
  <div class="container">
    <div class="row my-4">
      <h1 class="mt-4 col-6">{{ title }}</h1>
    </div>
    <div>
      <div class="content">
      <ul class="list-group list-group-flush d-inline-block mx-auto">
        <li class="list-group-item">Beljakov A., Bubrih D.V. Karielan kielen učebnikka. Mosku, 1934.</li>
        <li class="list-group-item"> Gromova L. Aiga lugie i paissa karielakši. Тверь, 2002.</li>
        <li class="list-group-item">Miloradova A.A., Smirnov P.P. Karielan kielen učebnikka. Mosku, 1933.</li>
        <li class="list-group-item">Neverov A. Pikkarazet raskuazat. Mosku, 1936.</li>
        <li class="list-group-item">Patrakka M. Šuuri kondie. Espoo, 2013.</li>
        <li class="list-group-item">Patrakka M., Ščerbakova T. Šygyžylahjat lapšilla. Петрозаводск, 2014.</li>
        <li class="list-group-item">Šoita, šoita, šoma šoittu (častuškoida tverinkarielakši). Петрозаводск, 2017.</li>
        <li class="list-group-item">Turičeva Z. Armaš šana. Тверь, 1996.</li>
        <li class="list-group-item">Yksi, kakši – karielakši (lapšin viržyzie tverinkarielakši). Петрозаводск, 2016.</li>
        <li class="list-group-item">Мои первые сто слов по-карельски (тверской говор карельского языка). Тверь, 2012.</li>
        <li class="list-group-item">Словарь карельского языка. Петрозаводск, 1994.</li>
        <li class="list-group-item">Тарасов С. Oma randa. Тверь, 2008.</li>
      </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BooksComponent',
  data() {
    return {
      title: 'Literatura',
      loading: false,
    };
  },
  mounted() {
    document.title = 'Literatura';
  }
};
</script>

<style scoped>
.content {
  margin-bottom: 20px;
}

h1 {
  margin-bottom: 10px;
}
</style>