<template>
  <v-app>
    <v-toolbar app>
      <v-toolbar-title class="toolbar-title">
        <router-link to="/">Cuizin</router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <router-link to="/new">
        <v-btn icon>
          <v-icon>add</v-icon>
        </v-btn>
      </router-link>
    </v-toolbar>
    <v-content>
      <router-view/>
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
.toolbar-title a {
  color: rgba(0,0,0,.87);
  text-decoration: none;
}
</style>
