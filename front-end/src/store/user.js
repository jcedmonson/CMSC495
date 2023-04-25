/**
 * Contains the logic and objects associated with user authentication and user data.
 * @namespace store.user
 * @author Jacob Edmonson
 */

import router from "@/router";
import { defineStore } from "pinia";
import { loginRequest, tokenCheck } from "@/scripts/user"
import { postStore } from "./posts";
import axios from "axios";
/**
 * User Store
 * @returns {Object}
 * @memberof store.user
 */
export const userStore = defineStore("user", {
  state: () => {
    return { 
      userId: "",
      username: "", 
      password: "", 
      first_name: "",
      last_name: "",
      email: "",
      connections: [],
      token: "",
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
      loginRequest({username: this.username, password: this.password}).then((resp) => {
        this.loggedIn = true;
        router.push("/");
      }).catch((e) => {
        router.push("/login")
      })
    },
    /**
     * Adds a connection "friend" to the user.
     * @param {Object} conn
     * @param {String} conn.username
     * @param {String} conn.userId
     * @function addConnection
     * @memberof store.user
     */
    addConnection(conn){
      axios.post(`auth/user/${this.userId}/connection`, conn).then((resp) => {
        this.connections.push(conn);
        const post = postStore();
        post.getPosts();
      }).catch((err) => {
        // notify user.
      })
    }
  },
});
