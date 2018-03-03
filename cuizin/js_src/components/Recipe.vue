<template>
  <v-container grid-list-md class="panel">
    <v-layout row>
      <v-flex xs12 v-if="recipe">
          <h1 class="text-xs-center mt-3 mb-3">
              {{ recipe.title }}
          </h1>
          <p>
          </p>
          <p class="text-xs-center">
              <img :src="recipe.picture" />
          </p>
          <v-layout row class="text-xs-center">
            <v-flex xs6>
                <p>{{ recipe.nb_person }}</p>
            </v-flex>
            <v-flex xs6>
              <p><v-icon>timelapse</v-icon> Preparation: {{ recipe.preparation_time }}&nbsp;mins</p>
              <p><v-icon>whatshot</v-icon> Cooking: {{ recipe.cooking_time }}&nbsp;mins</p>
            </v-flex>
          </v-layout>
          <p>{{ recipe.short_description }}</p>
          <h2>Ingredients</h2>
          <ul class="ml-5">
              <li v-for="ingredient in recipe.ingredients">
                  {{ ingredient }}
              </li>
          </ul>
          <h2 class="mt-3">Instructions</h2>
          <p>{{ recipe.instructions }}</p>
          <p v-if="recipe.url" class="text-xs-center">
              <v-btn :href="recipe.url">
                  <v-icon class="fa-icon">fa-external-link</v-icon>
              </v-btn>
              <v-btn @click="handleDelete">
                  <v-icon>delete</v-icon>
              </v-btn>
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

      fetch(`${constants.API_URL}api/v1/recipe/${this.$route.params.recipeId}`)
        .then(response => response.json())
        .then((response) => {
          this.recipe = response.recipes[0];
          this.isLoading = false;
        });
    },
    handleDelete() {
      fetch(`${constants.API_URL}api/v1/recipe/${this.$route.params.recipeId}`, {
        method: 'DELETE',
      })
        .then(() => this.$router.replace('/'));
    },
  },
};
</script>

<style scoped>
img {
    width: 100%;
}

.panel {
    max-width: 600px;
}

.fa-icon {
    font-size: 20px;
}
</style>
