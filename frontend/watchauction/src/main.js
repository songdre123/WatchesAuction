import { createApp } from 'vue'
import App from './App.vue'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
})

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas as all } from '@fortawesome/free-solid-svg-icons' // Adjust this import based on your specific needs

library.add(all)

const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(vuetify)
app.mount('#app')
