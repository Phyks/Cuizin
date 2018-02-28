<template>
  <v-container text-xs-center>
    <v-layout row wrap>
      <v-flex xs12>
        <h2>Import from URL</h2>
        <v-form v-model="validImport">
          <v-text-field
            label="URL"
            v-model="url"
            required
            :rules="urlRules"
            ></v-text-field>
          <v-btn
            @click="submitImport"
            :disabled="!validImport || disabledImport"
            >
            Import
          </v-btn>
        </v-form>
      </v-flex>
    </v-layout>
    <v-layout row wrap mt-5 v-if="featureAddManually">
      <v-flex xs12>
        <h2>Add manually</h2>
        <v-form v-model="validAdd">
          <v-text-field
            label="Title"
            v-model="title"
            required
            ></v-text-field>
          <v-text-field
            label="Picture"
            v-model="picture"
            ></v-text-field>
          <v-text-field
            label="Short description"
            v-model="short_description"
            textarea
            ></v-text-field>
          <v-layout row>
            <v-flex xs4 mr-3>
              <v-text-field
                label="Number of persons"
                v-model="nb_person"
                type="number"
                ></v-text-field>
            </v-flex>
            <v-flex xs4 mx-3>
              <v-text-field
                label="Preparation time"
                v-model="preparation_time"
                type="number"
                suffix="mins"
                ></v-text-field>
            </v-flex>
            <v-flex xs4 ml-3>
              <v-text-field
                label="Cooking time"
                v-model="cooking_time"
                type="number"
                suffix="mins"
                ></v-text-field>
            </v-flex>
          </v-layout>
          <v-text-field
            label="Ingredients"
            v-model="ingredients"
            textarea
            ></v-text-field>
          <v-text-field
            label="Instructions"
            v-model="instructions"
            textarea
            required
            ></v-text-field>

          <v-btn
            @click="submitAdd"
            :disabled="!validAdd"
            >
            Add
          </v-btn>
        </v-form>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import * as constants from '@/constants';


export default {
  data() {
    return {
      url: null,
      validImport: false,
      disabledImport: false,
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
      this.disabledImport = true;
      fetch(`${constants.API_URL}/api/v1/recipes`, {
        method: 'POST',
        body: JSON.stringify({
          url: this.url,
        }),
      })
        .then(response => response.json())
        .then(response => response.recipes[0])
        .then(recipe => this.$router.push({
          name: 'Recipe',
          params: {
            recipeId: recipe.id,
          },
        }));
    },
    submitAdd() {
      // TODO
    },
  },
};
</script>
