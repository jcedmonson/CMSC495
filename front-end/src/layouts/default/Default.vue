<template>
  <v-app>
    <system-message></system-message>
    <v-app-bar color="primary" v-if="router.currentRoute.value.name != 'Login'">
      <template v-slot:title>
        <v-icon>mdi-city</v-icon>
        CityPark
      </template>
      <!-- <v-avatar @click="" variant="elevated">{{ user.first_name[0]+user.last_name[0] }}</v-avatar> -->
      <v-btn icon="" elevation="3" style="background-color: #424242">{{
        user.first_name[0] + user.last_name[0]
      }}</v-btn>
    </v-app-bar>
    <default-view class="appBackground" />
  </v-app>
</template>

<script setup>
import DefaultView from "./View.vue";
import router from "@/router/index.js";
import SystemMessage from "@/components/system/SystemMessage";
import { userStore } from "@/store/user";
const user = userStore();
</script>
<style>
/* .appBackground{
  background: #01579B;
} */
</style>
