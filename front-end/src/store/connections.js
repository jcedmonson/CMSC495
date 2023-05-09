/**
 * Contains the logic and objects associated with post CRUD.
 * @namespace store.posts
 * @author Jacob Edmonson
 */

import axios from "axios";
import { defineStore } from "pinia";

import { userStore } from "@/store/user.js"

const USERS_SERVICE = import.meta.env.VITE_USERS_SERVICE;
const CONNECTIONS_SERVICE = import.meta.env.VITE_CONNECTIONS_SERVICE;

/**
 * Post Store
 * @returns {Object}
 * @memberof store.posts
 */
export const connectionsStore = defineStore("connections", {
  state: () => {
    return {
      users: [],
      connections: [],
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
     * @function getUsers
     * @memberof store.connections
     */
    getUsers() {
      console.log(USERS_SERVICE);
      axios.get(`${USERS_SERVICE}`).then((resp) => {
        this.users = resp.data;
      });
    },

    /**
     * Fetches users based on username.
     * @function getUser
     * @memberof store.connections
     */
    searchUsers(name) {
      axios.get(`${USERS_SERVICE}/${name}`).then((resp) => {
        this.users = resp.data
      }).catch((e) => {this.users = []});
    },

    /**
     * Fetches the connections for a specific user.
     * @function getConnections
     * @memberof store.connections
     */
    getConnections() {
      const user = userStore();
      return axios.get(`${CONNECTIONS_SERVICE}/user/${user.user_id}`).then((resp) => {
        this.connections = resp.data;
        return resp;
      });
    },

    /**
     * Adds a connection for a specific user.
     * @function addConnection
     * @memberof store.connections
     */
    addConnection(userObj){
      axios.post(`${CONNECTIONS_SERVICE}/user`, userObj).then((resp) => {
        this.connections.push(userObj)
      })
    },
  },
});
