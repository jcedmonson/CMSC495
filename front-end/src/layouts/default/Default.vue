<template>
  <v-app>
    <system-message></system-message>
    <v-app-bar color="primary" v-if="router.currentRoute.value.name != 'Login'">
      <v-app-bar-nav-icon
        @click="app.drawer = !app.drawer"
      ></v-app-bar-nav-icon>
      <v-app-bar-title>CityPark</v-app-bar-title>
      <!-- <v-progress-circular v-show="posts.loadingPosts" indeterminate class="mr-3"></v-progress-circular> -->
    </v-app-bar>
    <system-nav-drawer></system-nav-drawer>
    <default-view class="appBackground" />
  </v-app>
</template>

<script setup>
import DefaultView from "./View.vue";
import router from "@/router/index.js";
import SystemMessage from "@/components/system/SystemMessage";
import SystemNavDrawer from "@/components/system/SystemNavDrawer.vue";
import { appStore } from "@/store/app";
import { postStore } from "@/store/posts"
const app = appStore();
const posts = postStore();

</script>
<style>
/* .appBackground{
  background: #01579B;
} */
</style>
