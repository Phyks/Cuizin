'use strict'
const merge = require('webpack-merge')
const process = require('process');
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  API_URL: JSON.stringify(process.env.API_URL || "http://localhost:8080/"),
})
