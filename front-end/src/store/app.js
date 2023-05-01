/**
 * The main store for the app, handles getting the users.
 * @namespace store.app
 * @author Jacob Edmonson
 */

// Utilities
import axios from 'axios'
import { defineStore } from 'pinia'

/**
 * App Store
 * @returns {Object} appStore
 * @memberof store.app
 */
export const appStore = defineStore('app', {
  state: () => ({
    users: [],
    message: {
      content: "",
      show: false
    }
  }),
  actions: {
    /**
     * Fetches all of the users and sets them as the store array "users."
     * @function getUsers
     * @memberof store.app
     */
    getUsers(){
      const api = "http://192.168.131.2:5000"
      axios.get(`${api}/users`).then((resp) => {
        this.users = resp.data
      }).catch((err) => {
        // notify user

      })
    },

    showMessage(content){
      this.message.content = content;
      this.message.show = true;
      setTimeout(() => {
        this.message.show = false;
      }, 6000)
    }

  }
})
