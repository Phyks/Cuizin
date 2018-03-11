<template>
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
</template>

<script>
import * as api from '@/api';
import * as rules from '@/rules';

export default {
    props: {
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
        return {
            url: null,
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
    },
};
</script>

<style scoped>
.transparent {
    background: transparent;
}
</style>