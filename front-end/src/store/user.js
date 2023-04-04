import router from "@/router";
import { defineStore } from "pinia";
import { loginRequest, tokenCheck } from "@/scripts/user"
import { postStore } from "./posts";
import axios from "axios";

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
    login() {
      loginRequest({username: this.username, password: this.password}).then((resp) => {
        this.loggedIn = true;
        router.push("/");
      }).catch((e) => {
        router.push("/login")
      })
    },
    addConnection(conn){
      const api = "http://192.168.131.2:5000"
      axios.post(`${api}/user/${this.userId}/connection`, conn).then((resp) => {
        this.connections.push(conn);
        const post = postStore();
        post.getPosts();
      }).catch((err) => {
        // notify user.
      })
    }
  },
});
