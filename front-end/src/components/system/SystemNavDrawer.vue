<template>
  <v-navigation-drawer v-model="app.drawer" location="left" temporary>
    <v-list-item class="pt-2 pb-2" @click="router.push({name: 'Profile'})">
      <template v-slot:prepend>
        <v-avatar variant="elevated" color="primary">{{
          user.first_name[0] + user.last_name[0]
        }}</v-avatar>
      </template>
      <v-list-item-title> @{{ user.user_name }} </v-list-item-title>
    </v-list-item>
    <v-divider></v-divider>
    <v-list class="ml-2">
      <v-list-item v-for="(r, idx) in routes" :key="idx" @click="router.push({name: r.name})">
        <template v-slot:prepend>
          <v-icon :icon="r.icon"></v-icon>
        </template>
        <v-list-item-title> {{ r.name }} </v-list-item-title>
      </v-list-item>
    </v-list>
    <v-list-item class="ml-2" @click="user.logout">
        <template v-slot:prepend>
          <v-icon icon="mdi-logout"></v-icon>
        </template>
      <v-list-item-title> Logout </v-list-item-title>
    </v-list-item>
  </v-navigation-drawer>
</template>

<script setup>
import { appStore } from "@/store/app";
import { userStore } from "@/store/user";
import router from "@/router"; 
const user = userStore();
const app = appStore();

const routes = [
  { name: "Home", icon: "mdi-home", route: "/" },
  { name: "Connections", icon: "mdi-account-multiple", route: "/connections" },
];
</script>

<style></style>
