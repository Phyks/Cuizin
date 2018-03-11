<template>
    <v-flex xs12>
        <ErrorDialog v-model="error" :description="$t('error.unable_import_recipe')" />

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
</template>

<script>
import * as api from '@/api';
import * as rules from '@/rules';

import ErrorDialog from '@/components/ErrorDialog';

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
    components: {
        ErrorDialog,
    },
    data() {
        return {
            error: null,
            url: null,
            isValidImport: false,
            requiredUrlRules: Array.concat(
                [],
                [v => !!v || this.$t('new.url_is_required')],
                rules.url,
            ),
        };
    },
    methods: {
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
    },
};
</script>
