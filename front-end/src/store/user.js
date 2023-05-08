/**
 * Contains the logic and objects associated with user authentication and user data.
 * @namespace store.user
 * @author Jacob Edmonson
 */

import router from "@/router";
import { defineStore } from "pinia";
import { loginRequest, tokenCheck } from "@/scripts/user";
import { postStore } from "./posts";
import { appStore } from "@/store/app.js";
import axios from "axios";

const AUTH_SERVICE = import.meta.env.VITE_AUTH_SERVICE;

/**
 * User Store
 * @returns {Object}
 * @memberof store.user
 */
export const userStore = defineStore("user", {
  state: () => {
    return {
      loading: false,
      newUser: false,
      user_id: "",
      user_name: "",
      password: "",
      confirmPassword: "",
      first_name: "",
      last_name: "",
      email: "",
      connections: [],
      token: "",
      loginFormValid: false,
      newUserFormValid: false,
      loggedIn: false,
    };
  },

  actions: {
    /**
     * Login request to the server, uses scripts/user.js
     * @function login
     * @memberof store.user
     */
    login() {
      if (this.loginFormValid) {
        const app = appStore();

        loginRequest({ user_name: this.user_name, password: this.password })
          .then((resp) => {
            this.loggedIn = true;
            router.push("/");
          })
          .catch((e) => {
            router.push("/login");
            switch (e.response.status) {
              case 401:
                this.reset();
                app.showMessage("Incorrect Username Or Password.");
            }
          });
      }
    },

    /**
     * Resets the store and logs the user out.
     * @function login
     * @memberof store.user
     */
    logout() {
      sessionStorage.clear()
      this.reset();
      router.push("/login");
    },

    /**
     * Resets store state
     * @function reset
     * @memberof store.user
     */
    reset() {
      this.loading = false;
      this.newUser = false;
      this.user_id = "";
      this.user_name = "";
      this.password = "";
      this.first_name = "";
      this.last_name = "";
      this.email = "";
      this.connections = [];
      this.token = "";
      this.loggedIn = false;
      this.loginFormValid = false;
      this.newUserFormValid = false;
    },

    /**
     * Create a user
     * @function createUser
     * @memberof store.user
     */
    createUser() {
      const app = appStore();

      this.loading = true;

      if (this.newUserFormValid) {
        const newUserObj = {
          user_name: this.user_name,
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email,
          password: this.password,
        };

        return axios
          .post(`${AUTH_SERVICE}/user`, newUserObj)
          .then((resp) => {
            const message = "Account Created, Please Log In.";
            this.reset();
            app.showMessage(message);
          })
          .catch((err) => {
            // notify user
            this.reset();
            app.showMessage(err);
          });
      }
    },

    /**
     * Adds a connection "friend" to the user.
     * @param {Object} conn
     * @param {String} conn.user_name
     * @param {String} conn.user_id
     * @function addConnection
     * @memberof store.user
     */
    addConnection(conn) {
      axios
        .post(`${AUTH_SERVICE}/user/${this.user_id}/connection`, conn)
        .then((resp) => {
          this.connections.push(conn);
          const post = postStore();
          post.getPosts();
        })
        .catch((err) => {
          // notify user.
        });
    },
  },
});
