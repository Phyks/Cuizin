<template>
    <v-container fluid grid-list-md>
        <Loader v-if="isLoading"></Loader>
        <v-layout row wrap v-else>
            <ErrorDialog v-model="error" :description="$t('error.unable_load_recipes')" />

            <v-flex xs12 v-if="!error && !recipes.length" class="text-xs-center">
              <p>{{ $t('home.onboarding') }}</p>
            </v-flex>
            <v-flex
                v-for="recipe in recipes"
                :key="recipe.title"
                xs12 sm6 md3 lg2>
                <v-card :to="{name: 'Recipe', params: { recipeId: recipe.id }}">
                    <v-card-media :src="recipe.picture" height="200px" class="grey"></v-card-media>
                    <v-card-title primary-title>
                        <div>
                            <h3 class="headline mb-0">{{ recipe.title }}</h3>
                        </div>
                    </v-card-title>
                    <v-layout row text-xs-center wrap>
                        <v-flex xs12 v-if="recipe.short_description">
                            <p>{{ recipe.short_description }}</p>
                        </v-flex>
                        <v-flex xs6>
                          <p><v-icon>timelapse</v-icon> {{ $tc('misc.Nmins', recipe.preparation_time, { count: timeOrUnknown(recipe.preparation_time) }) }}</p>
                        </v-flex>
                        <v-flex xs6>
                            <p><v-icon>whatshot</v-icon> {{ $tc('misc.Nmins', recipe.cooking_time, { count: timeOrUnknown(recipe.cooking_time) }) }}</p>
                        </v-flex>
                    </v-layout>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
import * as api from '@/api';

import ErrorDialog from '@/components/ErrorDialog';
import Loader from '@/components/Loader';

export default {
    components: {
        ErrorDialog,
        Loader,
    },
    data() {
        return {
            isLoading: false,
            error: null,
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

            api.loadRecipes()
                .then((response) => {
                    this.recipes = response.recipes;
                    this.isLoading = false;
                })
                .catch((error) => {
                    this.error = error;
                    this.isLoading = false;
                });
        },
        timeOrUnknown(time) {
            if (time !== null && time !== undefined) {
                return time;
            }
            return '?';
        },
    },
};
</script>
