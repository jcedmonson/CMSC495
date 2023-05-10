/**
 * Contains the logic and objects associated with post CRUD.
 * @namespace store.posts
 * @author Jacob Edmonson
 */

import axios from "axios";
import { defineStore } from "pinia";
import { userStore } from "@/store/user";

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
      comment: "",
      loadingPosts: false,
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
     * Posts a reaction to the backend.
     * @function postComment
     * @memberof store.posts
     */
    postComment(){
      const user = userStore();
      if (this.comment.length > 0){
        return axios.post(`${POSTS_SERVICE}/${this.selectedPost.post_id}/comment`, {
          user_id: user.user_id,
          user_name: user.user_name,
          first_name: user.first_name,
          last_name: user.last_name,
          content: this.comment
        }).then((resp) => {
          this.viewPost(this.selectedPost.post_id)
          this.comment = "";
          return resp;
        });
      }
    },

    /**
     * Posts a reaction to the backend.
     * @function postReaction
     * @memberof store.posts
     */
    postReaction(post_id,reaction){
      const user = userStore();
      return axios.post(`${POSTS_SERVICE}/${post_id}/reaction`, {
        user_id: user.user_id,
        user_name: user.user_name,
        first_name: user.first_name,
        last_name: user.last_name,
        reaction: reaction,
      }).then((resp) => {
        this.getPosts();
        return resp;
      });
    },

    /**
     * Fetches all posts in the database and sets them as the currentPosts store value.
     * @function getPosts
     * @memberof store.posts
     */
    getPosts() {
      this.loadingPosts = true;
      return axios.get(`${POSTS_SERVICE}/timeline/`).then((resp) => {
        this.currentPosts = resp.data;
        setTimeout(() => {this.loadingPosts = false}, 3000)
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

    /**
     * Removes a post from the backend
     * @function deletePost
     * @memberof store.posts
     */
    deletePost(post_id){
      return axios.post(`${POSTS_SERVICE}/delete`, {post_id: post_id}).then((resp) => {
        this.getPosts();
        return resp;
      });
    }
  },
});
