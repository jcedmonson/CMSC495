// Utilities
import axios from 'axios'
import { defineStore } from 'pinia'

export const appStore = defineStore('app', {
  state: () => ({
    users: []
  }),
  actions: {
    getUsers(){
      const api = "http://192.168.131.2:5000"
      axios.get(`${api}/users`).then((resp) => {
        this.users = resp.data
      }).catch((err) => {
        // notify user
      })
    }
  }
})
