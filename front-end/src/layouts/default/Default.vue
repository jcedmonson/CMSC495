<template>
  <v-app>
    <v-app-bar title="CityPark" v-if="router.currentRoute.value.name != 'Login'">

      <v-avatar>{{ user.first_name[0]+user.last_name[0] }}</v-avatar>
    </v-app-bar>
    <default-view class="appBackground" />
  </v-app>
</template>

<script setup>
  import DefaultView from './View.vue'
  import router from "@/router/index.js"
  import { userStore } from "@/store/user";
  const user = userStore();

 


</script>
<style>
.appBackground{
  background: #263238;
}
</style>