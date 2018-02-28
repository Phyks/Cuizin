<template>
  <v-container grid-list-md>
    <v-layout row wrap>
      <v-flex xs6 offset-xs3>
          <h1 class="text-xs-center mt-3 mb-3">
              {{ this.recipe.title }}
              <v-btn @click="handleDelete">Delete</v-btn>
          </h1>
          <p class="text-xs-center">
              <img :src="this.recipe.picture" />
          </p>
          <v-layout row text-xs-center>
            <v-flex xs6>
              <p><v-icon>timelapse</v-icon> {{ recipe.preparation_time }} mins</p>
            </v-flex>
            <v-flex xs6>
              <p><v-icon>whatshot</v-icon> {{ recipe.cooking_time }} mins</p>
            </v-flex>
          </v-layout>
          <ul>
            <li v-for="ingredient in this.recipe.ingredients">
              {{ ingredient }}
            </li>
          </ul>
          <p>{{ this.recipe.nb_person }}</p>
          <p>{{ this.recipe.short_description }}</p>
          <p>{{ this.recipe.instructions }}</p>
          <p v-if="this.recipe.url">
              <a :href="this.recipe.url">Original link</a>
          </p>
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
    handleDelete() {
      fetch(`${constants.API_URL}/api/v1/recipe/${this.$route.params.recipeId}`, {
        method: 'DELETE',
      })
        .then(() => this.$router.replace('/'));
    },
  },
};
</script>

<style scoped>
img {
    width: 75%;
}
</style>
