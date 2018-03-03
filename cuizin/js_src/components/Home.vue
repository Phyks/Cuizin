<template>
  <v-container fluid grid-list-md>
    <v-layout row wrap>
      <v-flex
        v-for="recipe in recipes"
        :key="recipe.title"
        xs12
        sm6
        md3
        lg2
      >
        <v-card :to="{name: 'Recipe', params: { recipeId: recipe.id }}">
          <v-card-media :src="recipe.picture" height="200px"></v-card-media>
          <v-card-title primary-title>
            <div>
              <h3 class="headline mb-0">{{ recipe.title }}</h3>
            </div>
          </v-card-title>
          <p>{{ recipe.short_description }}</p>
          <v-layout row text-xs-center>
            <v-flex xs6>
              <p><v-icon>timelapse</v-icon> {{ recipe.preparation_time }} mins</p>
            </v-flex>
            <v-flex xs6>
              <p><v-icon>whatshot</v-icon> {{ recipe.cooking_time }} mins</p>
            </v-flex>
          </v-layout>
        </v-card>
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
      recipes: [],
    };
  },
  created() {
    this.fetchRecipes();
  },
  watch: {
    // call again the method if the route changes
    $route: 'fetchRecipes',
  },
  methods: {
    fetchRecipes() {
      this.isLoading = true;

      fetch(`${constants.API_URL}api/v1/recipes`)
        .then(response => response.json())
        .then((response) => {
          this.recipes = response.recipes;
          this.isLoading = false;
        });
    },
  },
};
</script>
