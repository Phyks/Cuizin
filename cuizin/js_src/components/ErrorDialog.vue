<template>
    <v-dialog v-if="error" v-model="error" max-width="500px">
        <v-card>
            <v-card-title class="headline">Error</v-card-title>
            <v-card-text>
                {{ description }} {{ value.message }}.
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="secondary" flat @click.stop="error=null">Cancel</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
export default {
    props: {
        description: String,
        value: [Error, Boolean],
    },
    computed: {
        error: {
            get() {
                return this.value;
            },
            set(val) {
                this.$emit('input', val);
            },
        },
    },
};
</script>
