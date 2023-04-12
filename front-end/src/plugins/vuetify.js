/**
 * @module vuetify
 * @description Creates vuetify, exports the plugin.
 * @author Jacob Edmonson
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    themes: {
      light: {
        colors: {
          primary: '#263238',
          secondary: '#5CBBF6',
        },
      },
    },
  },
})
