import * as constants from '@/constants';


function loadJSON(response) {
    return response.json();
}


function _postProcessRecipes(response) {
    return loadJSON(response)
        .then((jsonResponse) => {
            const parsed = jsonResponse;

            if (parsed.recipes) {
                // Customize instructions
                parsed.recipes = parsed.recipes.map(item => Object.assign(
                    item,
                    {
                        instructions: item.instructions ? item.instructions.split(/[\r\n]\n/).map(
                            line => line.trim(),
                        ) : [],
                    },
                ));
            }

            return parsed;
        });
}


export function loadRecipes() {
    return fetch(`${constants.API_URL}api/v1/recipes`, { credentials: 'same-origin' })
        .then(_postProcessRecipes);
}


export function loadRecipe(id) {
    return fetch(`${constants.API_URL}api/v1/recipe/${id}`, { credentials: 'same-origin' })
        .then(_postProcessRecipes);
}


export function refetchRecipe(id) {
    return fetch(
        `${constants.API_URL}api/v1/recipe/${id}/refetch`,
        { credentials: 'same-origin' },
    )
        .then(_postProcessRecipes);
}


export function postRecipeByUrl(recipe) {
    return fetch(`${constants.API_URL}api/v1/recipes/by_url`, {
        method: 'POST',
        body: JSON.stringify(recipe),
        credentials: 'same-origin',
    })
        .then(_postProcessRecipes);
}


export function postRecipeManually(recipe) {
    return fetch(`${constants.API_URL}api/v1/recipes/manually`, {
        method: 'POST',
        body: JSON.stringify(recipe),
        credentials: 'same-origin',
    })
        .then(_postProcessRecipes);
}


export function editRecipe(id, recipe) {
    return fetch(`${constants.API_URL}api/v1/recipe/${id}`, {
        method: 'POST',
        body: JSON.stringify(recipe),
        credentials: 'same-origin',
    })
        .then(_postProcessRecipes);
}


export function deleteRecipe(id) {
    return fetch(`${constants.API_URL}api/v1/recipe/${id}`, {
        method: 'DELETE',
        credentials: 'same-origin',
    });
}
