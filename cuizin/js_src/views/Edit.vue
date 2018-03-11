<template>
    <v-container text-xs-center v-if="isLoading">
        <v-layout row>
            <Loader></Loader>
        </v-layout>
    </v-container>
    <v-container text-xs-center v-else-if="isImporting">
        <v-layout row wrap>
            <Loader></Loader>

            <v-flex xs12>
                <p>{{ $t('new.updating') }}</p>
            </v-flex>
        </v-layout>
    </v-container>
    <v-container text-xs-center v-else class="panel">
        <v-layout row wrap>
            <EditForm v-model="isImporting" :recipe="recipe"></EditForm>
        </v-layout>
    </v-container>
</template>

<script>
import * as api from '@/api';

import EditForm from '@/components/EditForm';
import Loader from '@/components/Loader';


export default {
    components: {
        EditForm,
        Loader,
    },
    data() {
        return {
            isImporting: false,
            isLoading: false,
            error: null,
            recipe: null,
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
                    this.error = error;
                });
        },
    },
};
</script>
