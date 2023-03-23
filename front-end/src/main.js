/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from "./App.vue";
import router from "@/router";
import { userData } from "@/store/user";

// Composables
import { createApp } from "vue";

// Plugins
import { registerPlugins } from "@/plugins";

const app = createApp(App);

registerPlugins(app);

const user = userData();

router.beforeEach((to, from, next) => {
  console.log(user.loggedIn);
  if (user.loggedIn) {
    document.title = to.name;
    next();
  } else {
    if (to.path != "/login") {
      document.title = to.name;
      router.push("/login");
    } else {
      document.title = to.name;
      next();
    }
  }
});

app.mount("#app");
