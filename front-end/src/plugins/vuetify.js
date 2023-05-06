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
    defaultTheme: 'dark',
    themes: {
      light: {
        colors: {
          primary: '#0288D1',
          secondary: '#212121',
        },
      },
      dark: {
        colors: {
          primary: '#5C6BC0',
          secondary: '#424242',
        },
      }
    },
  },
})
