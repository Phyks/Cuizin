<template>
    <v-container text-xs-center v-if="isImporting">
        <v-layout row wrap>
            <Loader></Loader>

            <v-flex xs12>
                <p>{{ $t('new.importing') }}</p>
            </v-flex>
        </v-layout>
    </v-container>
    <v-container text-xs-center v-else class="panel">
        <v-layout row wrap>
            <ErrorDialog v-model="error" :description="$t('error.unable_import_recipe')" />

            <v-flex xs12>
                <h2>{{ $t('new.import_from_url') }}</h2>
                <v-form v-model="isValidImport">
                    <v-text-field
                        label="URL"
                        v-model="url"
                        required
                        :rules="requiredUrlRules"
                        ></v-text-field>
                    <v-btn
                        @click="submitImport"
                        :disabled="!isValidImport || isImporting"
                        >
                        {{ $t('new.import') }}
                    </v-btn>
                </v-form>
            </v-flex>
        </v-layout>
        <v-layout row wrap mt-5>
            <v-flex xs12>
                <h2>{{ $t('new.add_manually') }}</h2>
                <v-form v-model="isValidAdd">
                    <v-text-field
                        :label="$t('new.title')"
                        v-model="title"
                        required
                        :rules="[v => !!v || $t('new.title_is_required')]"
                        ></v-text-field>
                    <v-text-field
                        :label="$t('new.picture_url')"
                        v-model="picture_url"
                        :rules="urlRules"
                        ></v-text-field>
                    <v-text-field
                        :label="$t('new.short_description')"
                        v-model="short_description"
                        textarea
                        ></v-text-field>
                    <v-layout row wrap>
                        <v-flex xs12 md5>
                            <v-text-field
                                :label="$t('new.preparation_time')"
                                v-model="preparation_time"
                                type="number"
                                :suffix="$t('new.mins')"
                                ></v-text-field>
                        </v-flex>
                        <v-flex xs12 md5 offset-md2>
                            <v-text-field
                                :label="$t('new.cooking_time')"
                                v-model="cooking_time"
                                type="number"
                                :suffix="$t('new.mins')"
                                ></v-text-field>
                        </v-flex>
                    </v-layout>
                    <v-text-field
                        :label="$t('new.nb_persons')"
                        v-model="nb_person"
                        ></v-text-field>
                    <v-layout row>
                        <v-flex xs12 class="text-xs-left">
                            <h3>{{ $t('new.ingredients') }}</h3>
                            <v-list v-if="ingredients.length" class="transparent">
                                <v-list-tile v-for="ingredient in ingredients" :key="ingredient">
                                    <v-list-tile-action>
                                        <v-btn flat icon color="red" v-on:click="() => removeIngredient(ingredient)">
                                            <v-icon>delete</v-icon>
                                        </v-btn>
                                    </v-list-tile-action>
                                    <v-list-tile-content>
                                        <v-list-tile-title>{{ ingredient }}</v-list-tile-title>
                                    </v-list-tile-content>
                                </v-list-tile>
                            </v-list>
                            <p class="ml-5 my-3" v-else>{{ $t('new.none') }}</p>
                            <v-text-field
                                :label="$t('new.add_ingredient')"
                                v-model="new_ingredient"
                                @keyup.enter.native="addIngredient"
                                ></v-text-field>
                        </v-flex>
                    </v-layout>
                    <v-text-field
                        :label="$t('new.instructions')"
                        v-model="instructions"
                        :rules="[v => !!v || $t('new.instructions_are_required')]"
                        textarea
                        required
                        ></v-text-field>

                    <v-btn
                        @click="submitAdd"
                        :disabled="!isValidAdd || isImporting"
                        >
                        {{ $t('new.add') }}
                    </v-btn>
                </v-form>
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
        const urlRules = [
            (v) => {
                if (!v) {
                    return true;
                }
                try {
                    new URL(v);  // eslint-disable-line no-new
                    return true;
                } catch (e) {
                    return this.$t('new.url_must_be_valid');
                }
            },
        ];
        return {
            error: null,
            url: null,
            isValidImport: false,
            isImporting: false,
            isValidAdd: false,
            title: null,
            picture_url: null,
            short_description: null,
            nb_person: null,
            preparation_time: null,
            cooking_time: null,
            new_ingredient: null,
            ingredients: [],
            instructions: null,
            requiredUrlRules: Array.concat(
                [],
                [v => !!v || this.$t('new.url_is_required')],
                urlRules,
            ),
            urlRules,
        };
    },
    methods: {
        addIngredient() {
            this.ingredients.push(this.new_ingredient);
            this.new_ingredient = null;
        },
        removeIngredient(ingredient) {
            const index = this.ingredients.indexOf(ingredient);
            if (index !== -1) {
                this.ingredients.splice(index, 1);
            }
        },
        submitImport() {
            this.isImporting = true;
            api.postRecipeByUrl({ url: this.url })
                .then(response => this.$router.push({
                    name: 'Recipe',
                    params: {
                        recipeId: response.recipes[0].id,
                    },
                }))
                .catch((error) => {
                    this.isImporting = false;
                    this.error = error;
                });
        },
        submitAdd() {
            this.isImporting = true;
            api.postRecipeManually({
                title: this.title,
                picture_url: this.picture_url,
                short_description: this.short_description,
                preparation_time: this.preparation_time,
                cooking_time: this.cooking_time,
                nb_person: this.nb_person,
                ingredients: this.ingredients,
                instructions: this.instructions,
            })
                .then(response => this.$router.push({
                    name: 'Recipe',
                    params: {
                        recipeId: response.recipes[0].id,
                    },
                }))
                .catch((error) => {
                    this.isImporting = false;
                    this.error = error;
                });
        },
    },
};
</script>

<style scoped>
.transparent {
    background: transparent;
}
</style>
