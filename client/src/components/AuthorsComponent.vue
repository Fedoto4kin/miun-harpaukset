<template>
  <div class="container">
    <div class="row my-4">
      <h1 class="mt-4 col-6">
        <font-awesome-icon :icon="['fas', 'users']" class="text-success" />
        {{ title }}
      </h1>
    </div>
    <div>
      <div class="content">
        <table class="table">
          <tbody>
            <tr>
              <th scope="row">Web-programmista:</th>
              <td>
                <b>Anatolii Fedotočkin</b> 
                (<a href="mailto:fedoto4kin@gmail.com">fedoto4kin@gmail.com</a>)
              </td>
            </tr>
            <tr>
              <th scope="row">Šanakniigan keriäjät:</th>
              <td>
                <b>Irina Novak</b>, <b>Irina Komissarova</b>
              </td>
            </tr>
            <tr>
              <th scope="row">Iänehlugija:</th>
              <td>
                <b>Irina Komissarova</b><br />
                <a href="https://vk.com/startmusictver" target="_blank">StArt-iänehstudija</a>, Tveri-linna
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthorsComponent',
  data() {
    return {
      title: 'Luadijat',
      loading: false,
    };
  },
  mounted() {
    document.title = 'Luadijat';
  }
};
</script>

<style scoped>
.content {
  margin-bottom: 20px;
}

h1 {
  margin-bottom: 20px;
}

.btn {
  margin-top: 20px;
}

.table {
  width: 100%;
  max-width: 600px;
}

.table th {
  width: 40%;   
  text-align: right;
  vertical-align: top;
  padding-right: 15px;
}

.table td {
  text-align: left;
}
</style>