import router from "@/router";
import { defineStore } from "pinia";

export const userData = defineStore("user", {
  state: () => {
    return { 
      username: "", 
      password: "", 
      firstName: "",
      lastName: "",
      email: "",
      token: "",
      loggedIn: false 
    };
  },

  actions: {
    login() {
      console.log([this.username, this.password]);
      this.loggedIn = true;
      router.push("/");
    },
  },
});
