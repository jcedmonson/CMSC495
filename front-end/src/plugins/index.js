/**
 * @module plugins
 * @description loads the vuetify, pinia, and vue router into the vue appliation.
 * @author Jacob Edmonson
 */

// Plugins
import { loadFonts } from './webfontloader'
import vuetify from './vuetify'
import pinia from '../store'
import router from '../router'

export function registerPlugins (app) {
  loadFonts()
  app
    .use(vuetify)
    .use(pinia)
    .use(router)
}
