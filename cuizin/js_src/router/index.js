import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/views/Home';
import New from '@/views/New';
import Recipe from '@/views/Recipe';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Home',
            component: Home,
        },
        {
            path: '/new',
            name: 'New',
            component: New,
        },
        {
            path: '/recipe/:recipeId',
            name: 'Recipe',
            component: Recipe,
        },
    ],
});
