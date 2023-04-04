/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from "./App.vue";
import router from "@/router";
import { userStore } from "@/store/user";
import { tokenCheck } from "@/scripts/user";

// Composables
import { createApp } from "vue";

// Plugins
import { registerPlugins } from "@/plugins";

const app = createApp(App);

registerPlugins(app);

const user = userStore();

router.beforeEach((to, from, next) => {
  const token = sessionStorage.getItem("city_park_token");

  if (user.loggedIn) {
    document.title = to.name;
    next();
  } else {
    // if the store does not annotate the user as logged in,
    if (to.path != "/login") {
      // check token
      tokenCheck(token)
    } else {
      document.title = to.name;
      next();
    }
  }
});

app.mount("#app");
