/**
 * Contains the logic and objects associated with post CRUD.
 * @namespace store.posts
 * @author Jacob Edmonson
 */

import axios from "axios";
import { defineStore } from "pinia";

const USERS_SERVICE = import.meta.env.VITE_USERS_SERVICE;

/**
 * Post Store
 * @returns {Object}
 * @memberof store.posts
 */
export const connectionsStore = defineStore("connections", {
  state: () => {
    return {
        users: []
    };
  },
  actions: {
    /**
     * Fetches a specific post
     * @function viewPost
     * @memberof store.posts
     */
    viewPost(id) {
      const api = "http://192.168.131.2:5000";
      return axios
        .get(`${api}/posts/${id}`)
        .then((resp) => {
          this.selectedPost = resp.data;
        })
        .catch((err) => {
          this.selectedPost = err;
        });
    },

    /**
     * Fetches all of the app's users.
     * @function viewPost
     * @memberof store.posts
     */
    getUsers() {
      console.log(USERS_SERVICE);
      axios.get(`${USERS_SERVICE}`).then((resp) => {
        this.users = resp.data;
      });
    },

    /**
     * Fetches a user by username.
     * @function viewPost
     * @memberof store.posts
     */
    getUser(name) {
      axios.get(`${USERS_SERVICE}/${name}`).then((resp) => {
        console.log(resp.data);
      });
    },
  },
});
