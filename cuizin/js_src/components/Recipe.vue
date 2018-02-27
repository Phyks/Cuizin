<template>
  <v-container grid-list-md>
    <v-layout row wrap>
      <v-flex xs12 v-if="this.recipe">
          <h1>{{ this.recipe.title }}</h1>
          <p><img :src="this.recipe.picture" height="300px" /></p>
          <p>{{ this.recipe.short_description }}</p>
          <p>{{ this.recipe.ingredients }}</p>
          <p>{{ this.recipe.instructions }}</p>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import * as constants from '@/constants';

export default {
  data() {
    return {
      isLoading: false,
      recipe: null,
    };
  },
  created() {
    this.fetchRecipe();
  },
  watch: {
    // call again the method if the route changes
    $route: 'fetchRecipe',
  },
  methods: {
    fetchRecipe() {
      this.isLoading = true;

      fetch(`${constants.API_URL}/api/v1/recipe/${this.$route.params.recipeId}`)
        .then(response => response.json())
        .then((response) => {
          this.recipe = response.recipes[0];
          this.isLoading = false;
        });
    },
  },
};
</script>
