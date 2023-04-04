import axios from "axios";
import { defineStore } from "pinia";

export const postStore = defineStore("posts", {
  state: () => {
    return {
      currentPosts: [],
      post: ""
    }
  },
  actions: {
    getPosts(){
      const api = "http://192.168.131.2:5000"
      axios.get(`${api}/posts`).then((resp) => {
        this.currentPosts = resp.data;
      })
    },

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