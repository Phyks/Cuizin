<template>
    <v-list-tile>
        <v-list-tile-action>
            <v-btn flat icon color="red" v-on:click="onDelete">
                <v-icon>delete</v-icon>
            </v-btn>
        </v-list-tile-action>
        <v-list-tile-content>
            <v-list-tile-title v-on:click="(editable === false) && (editable = true)">
                <v-text-field v-if="editable"
                    v-model="updatedIngredient"
                    single-line
                    solo
                    @keyup.enter.native="editIngredient"
                    ></v-text-field>
                <template v-else>
                    {{ ingredient }}
                </template>
            </v-list-tile-title>
        </v-list-tile-content>
    </v-list-tile>
</template>

<script>
export default {
    props: {
        ingredient: String,
        onDelete: Function,
        onEdit: Function,
    },
    data() {
        return {
            editable: false,
            updatedIngredient: this.ingredient,
        };
    },
    methods: {
        editIngredient() {
            this.editable = !this.editable;
            this.onEdit(this.updatedIngredient);
        },
    },
};
</script>
