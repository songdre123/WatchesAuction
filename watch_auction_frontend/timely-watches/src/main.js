/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from "./App.vue";

// Composables
import { createApp } from "vue";

// Plugins
import { registerPlugins } from "@/plugins";

import { registerLicense } from '@syncfusion/ej2-base';
import 'bootstrap/dist/css/bootstrap.css'; 

// Load environment variables from .env file

const app = createApp(App);

registerPlugins(app);


app.mount("#app");
registerLicense('Ngo9BigBOggjHTQxAR8/V1NBaF5cXmZCekx3Q3xbf1x0ZFREal9ZTnZXUiweQnxTdEFjWn5ZcHRRRGBcVER0WQ==')
