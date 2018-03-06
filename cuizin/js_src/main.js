// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import Vuetify from 'vuetify';
import VueI18n from 'vue-i18n';
import 'roboto-fontface/css/roboto/roboto-fontface.css';
import 'font-awesome/css/font-awesome.css';
import 'material-design-icons/iconfont/material-icons.css';
import 'vuetify/dist/vuetify.min.css';

import App from './App';
import messages from './i18n';
import router from './router';
import { getBestMatchingLocale } from './helpers';

// Isomorphic fetch
require('es6-promise').polyfill();
require('isomorphic-fetch');

Vue.use(Vuetify);
Vue.use(VueI18n);

Vue.config.productionTip = false;

const i18n = new VueI18n({
    locale: getBestMatchingLocale(messages),
    messages,
});

/* eslint-disable no-new */
new Vue({
    el: '#app',
    i18n,
    router,
    components: { App },
    template: '<App/>',
});
