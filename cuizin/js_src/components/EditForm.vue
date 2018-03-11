<template>
    <v-flex xs12>
        <ErrorDialog :v-model="error" :description="$t('error.title')" />

        <h2 v-if="recipe">{{ $t('new.edit_recipe') }}</h2>
        <h2 v-else>{{ $t('new.add_manually') }}</h2>

        <v-form v-model="isValidForm">
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
            <p>
                <img :src="picture_url" />
            </p>
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
                @click="submitEdit"
                :disabled="!isValidForm || isImporting"
                v-if="recipe"
                >
                {{ $t('new.edit') }}
            </v-btn>
            <v-btn
                @click="submitAdd"
                :disabled="!isValidForm || isImporting"
                v-else
                >
                {{ $t('new.add') }}
            </v-btn>
        </v-form>
    </v-flex>
</template>

<script>
import * as api from '@/api';
import * as rules from '@/rules';

import ErrorDialog from '@/components/ErrorDialog';

export default {
    components: {
        ErrorDialog,
    },
    props: {
        recipe: {
            default: null,
            type: Object,
        },
        value: Boolean,
    },
    computed: {
        isImporting: {
            get() {
                return this.value;
            },
            set(val) {
                this.$emit('input', val);
            },
        },
    },
    data() {
        let defaultPreparationTime = null;
        if (this.recipe &&
            this.recipe.preparation_time !== null && this.recipe.preparation_time !== undefined
        ) {
            defaultPreparationTime = this.recipe.preparation_time;
        }
        let defaultCookingTime = null;
        if (this.recipe &&
            this.recipe.cooking_time !== null && this.recipe.cooking_time !== undefined
        ) {
            defaultCookingTime = this.recipe.cooking_time;
        }
        return {
            error: null,
            url: null,
            isValidForm: false,
            title: (this.recipe && this.recipe.title) || null,
            picture_url: (this.recipe && this.recipe.picture) || null,
            short_description: (this.recipe && this.recipe.short_description) || null,
            nb_person: (this.recipe && this.recipe.nb_person) || null,
            preparation_time: defaultPreparationTime,
            cooking_time: defaultCookingTime,
            new_ingredient: null,
            ingredients: (this.recipe && this.recipe.ingredients) || [],
            instructions: (this.recipe && this.recipe.instructions.join('\n\n').replace(/\n{2,}/, '\n\n')) || null,
            urlRules: rules.url,
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
        submitEdit() {
            this.isImporting = true;
            api.editRecipe(this.recipe.id, {
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

img {
    max-height: 150px;
}
</style>
