<template>
    <v-container text-xs-center v-if="isImporting">
        <v-layout row wrap>
            <Loader></Loader>

            <v-flex xs12>
                <p>{{ $t('new.importing') }}</p>
            </v-flex>
        </v-layout>
    </v-container>
    <v-container text-xs-center v-else>
        <v-layout row wrap>
            <ErrorDialog v-model="error" :description="$t('error.unable_import_recipe')" />

            <v-flex xs12>
                <h2>{{ $t('new.import_from_url') }}</h2>
                <v-form v-model="validImport">
                    <v-text-field
                        label="URL"
                        v-model="url"
                        required
                        :rules="urlRules"
                        ></v-text-field>
                    <v-btn
                        @click="submitImport"
                        :disabled="!validImport || isImporting"
                        >
                        {{ $t('new.import') }}
                    </v-btn>
                </v-form>
            </v-flex>
        </v-layout>
        <v-layout row wrap mt-5 v-if="featureAddManually">
            <v-flex xs12>
                <h2>{{ $t('new.add_manually') }}</h2>
                <v-form v-model="validAdd">
                    <v-text-field
                        :label="$t('new.title')"
                        v-model="title"
                        required
                        ></v-text-field>
                    <v-text-field
                        :label="$t('new.picture')"
                        v-model="picture"
                        ></v-text-field>
                    <v-text-field
                        :label="$t('new.short_description')"
                        v-model="short_description"
                        textarea
                        ></v-text-field>
                    <v-layout row>
                        <v-flex xs4 mr-3>
                            <v-text-field
                                :label="$t('new.nb_persons')"
                                v-model="nb_person"
                                type="number"
                                ></v-text-field>
                        </v-flex>
                        <v-flex xs4 mx-3>
                            <v-text-field
                                :label="$t('new.preparation_time')"
                                v-model="preparation_time"
                                type="number"
                                :suffix="$t('new.mins')"
                                ></v-text-field>
                        </v-flex>
                        <v-flex xs4 ml-3>
                            <v-text-field
                                :label="$t('new.cooking_time')"
                                v-model="cooking_time"
                                type="number"
                                :suffix="$t('new.mins')"
                                ></v-text-field>
                        </v-flex>
                    </v-layout>
                    <v-text-field
                        :label="$t('new.ingredients')"
                        v-model="ingredients"
                        textarea
                        ></v-text-field>
                    <v-text-field
                        :label="$t('new.instructions')"
                        v-model="instructions"
                        textarea
                        required
                        ></v-text-field>

                    <v-btn
                        @click="submitAdd"
                        :disabled="!validAdd"
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
        return {
            error: null,
            url: null,
            validImport: false,
            isImporting: false,
            validAdd: false,
            title: null,
            picture: null,
            short_description: null,
            nb_person: null,
            preparation_time: null,
            cooking_time: null,
            ingredients: null,
            instructions: null,
            urlRules: [
                v => !!v || 'URL is required',
                (v) => {
                    try {
                        new URL(v);  // eslint-disable-line no-new
                        return true;
                    } catch (e) {
                        return 'URL must be valid';
                    }
                },
            ],
            featureAddManually: false,
        };
    },
    methods: {
        submitImport() {
            this.isImporting = true;
            api.postRecipe({ url: this.url })
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
            // TODO
        },
    },
};
</script>
