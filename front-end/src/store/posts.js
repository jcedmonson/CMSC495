/**
 * Contains the logic and objects associated with post CRUD.
 * @namespace store.posts
 * @author Jacob Edmonson
 */

import axios from "axios";
import { defineStore } from "pinia";

const POSTS_SERVICE = import.meta.env.VITE_POSTS_SERVICE;

/**
 * Post Store
 * @returns {Object}
 * @memberof store.posts
 */
export const postStore = defineStore("posts", {
  state: () => {
    return {
      currentPosts: [],
      post: "",
      selectedPost: {},
    };
  },
  actions: {
    /**
     * Fetches a specific post
     * @function viewPost
     * @memberof store.posts
     */
    viewPost(id) {
      return axios.get(`${POSTS_SERVICE}/${id}`).then((resp) => {
        this.selectedPost = resp.data;
      });
    },

    /**
     * Fetches all posts in the database and sets them as the currentPosts store value.
     * @function getPosts
     * @memberof store.posts
     */
    getPosts() {
      return axios.get(`${POSTS_SERVICE}/timeline/`).then((resp) => {
        this.currentPosts = resp.data;
        return resp;
      });
    },

    /**
     * Sends the user's post content to the server.
     * @function submitPost
     * @param {number|string} post
     * @memberof store.posts
     */
    submitPost() {
      if (this.post.length > 0) {
        axios
          .post(`${POSTS_SERVICE}`, { content: this.post })
          .then((resp) => {
            this.post = "";
            this.getPosts();
          })
          .catch((err) => {
            // notify user
          });
      }
    },
  },
});
