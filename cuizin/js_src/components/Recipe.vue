<template>
    <v-container grid-list-md class="panel">
        <Loader v-if="isLoading"></Loader>
        <v-layout row v-else>
            <ErrorDialog :v-model="errorDelete" description="Unable to delete recipe: " />
            <ErrorDialog :v-model="errorFetch" description="Unable to fetch recipe: " />
            <ErrorDialog :v-model="errorRefetch" description="Unable to refetch recipe: " />

            <v-dialog v-model="refetchConfirm" max-width="500px">
                <v-card>
                    <v-card-title class="headline">Refetch recipe</v-card-title>
                    <v-card-text>
                        This will refetch the recipe from the website and replace all current data with newly fetched ones. Are you sure?
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="secondary" flat @click.stop="refetchConfirm=false">Cancel</v-btn>
                        <v-btn color="error" flat @click.stop="handleRefetch">Refetch</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>

            <v-dialog v-model="deleteConfirm" max-width="500px">
                <v-card>
                    <v-card-title class="headline">Delete recipe</v-card-title>
                    <v-card-text>This will delete this recipe. Are you sure?</v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="secondary" flat @click.stop="deleteConfirm=false">Cancel</v-btn>
                        <v-btn color="error" flat @click.stop="handleDelete">Delete</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>

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
                <p v-for="item in recipe.instructions">
                    {{ item }}
                </p>
                <p v-if="recipe.url" class="text-xs-center">
                    <v-btn :href="recipe.url">
                        <v-icon class="fa-icon">fa-external-link</v-icon>
                    </v-btn>
                    <v-btn @click.stop="deleteConfirm = true">
                        <v-icon>delete</v-icon>
                    </v-btn>
                    <v-btn @click.stop="refetchConfirm = true">
                        <v-icon>autorenew</v-icon>
                    </v-btn>
                </p>
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
            recipe: null,
            errorFetch: null,
            errorDelete: null,
            errorRefetch: null,
            deleteConfirm: false,
            refetchConfirm: false,
        };
    },
    created() {
        this.loadRecipe();
    },
    watch: {
        // call again the method if the route changes
        $route: 'loadRecipe',
    },
    methods: {
        handleRecipesResponse(response) {
            if (response.recipes.length < 1) {
                this.$router.replace({
                    name: 'Home',
                });
            }
            this.recipe = response.recipes[0];
            this.isLoading = false;
        },
        loadRecipe() {
            this.isLoading = true;

            api.loadRecipe(this.$route.params.recipeId)
                .then(this.handleRecipesResponse)
                .catch((error) => {
                    this.isLoading = false;
                    this.errorFetch = error;
                });
        },
        handleDelete() {
            this.isLoading = true;
            this.deleteConfirm = false;
            api.deleteRecipe(this.$route.params.recipeId)
                .then(() => this.$router.replace('/'))
                .catch((error) => {
                    this.isLoading = false;
                    this.errorDelete = error;
                });
        },
        handleRefetch() {
            this.isLoading = true;
            this.refetchConfirm = false;

            api.refetchRecipe(this.$route.params.recipeId)
                .then(this.handleRecipesResponse)
                .catch((error) => {
                    this.isLoading = false;
                    this.errorRefetch = error;
                });
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
