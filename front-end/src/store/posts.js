/**
 * Contains the logic and objects associated with post CRUD.
 * @namespace store.posts
 * @author Jacob Edmonson
 */

import axios from "axios";
import { defineStore } from "pinia";

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
    }
  },
  actions: {

    /**
     * Fetches a specific post 
     * @function viewPost
     * @memberof store.posts
     */
    viewPost(id){
      const api = "http://192.168.131.2:5000"
      return axios.get(`${api}/posts/${id}`).then((resp) => {
        this.selectedPost = resp.data;
      }).catch((err) => {
        this.selectedPost = err;
      })
    },

    /**
     * Fetches all posts in the database and sets them as the currentPosts store value.
     * @function getPosts
     * @memberof store.posts
     */
    getPosts(){
      const api = "http://192.168.131.2:5000"
      axios.get(`${api}/posts`).then((resp) => {
        this.currentPosts = resp.data;
      })
    },

    /**
     * Sends the user's post content to the server.
     * @function submitPost
     * @param {number|string} post
     * @memberof store.posts
     */
    submitPost(post){
      const api = "http://192.168.131.2:5000"
      axios.post(`${api}/posts`, post).then((resp) => {
        this.post = "";
        this.currentPosts.unshift(resp.data)
      }).catch((err) => {
        // notify user
      })
    }
  }
})