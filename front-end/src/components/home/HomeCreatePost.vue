<template>
  <v-card >
    <v-card-title class="font-weight-light pb-3 pt-3">
      <v-avatar size="35" variant="elevated" color="primary" class="mr-1">{{
        user.first_name[0] + user.last_name[0]
      }}</v-avatar>

      @{{ user.user_name }}</v-card-title
    >

    <v-text-field
      class="pl-4 pr-4 pt-2 pb-1"
      color="primary"
      variant="outlined"
      label="What are you thinking?"
      @keypress.enter="posts.submitPost()"
      v-model="posts.post"
    ></v-text-field>
    <v-btn
      variant="text"
      @click="
        posts.submitPost()
      "
      >Post</v-btn
    >
  </v-card>
</template>

<script setup>
import { postStore } from "@/store/posts.js";
import { userStore } from "@/store/user";

const posts = postStore();
const user = userStore();
</script>

<style></style>
