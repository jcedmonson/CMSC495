<template>
  <v-card>
    <v-card-title class="font-weight-light">
      @{{ user.username }}
    </v-card-title>

      <v-text-field class="pl-4 pr-4 pt-2" variant="outlined" label="What are you thinking?" v-model="posts.post"></v-text-field>
      <v-btn class="pb-4" variant="text" @click="() => {
        posts.post.length > 0 ? posts.submitPost({
          userId : user.userId,
          username: user.username,
          content: posts.post
        }) : ''
      }">Post</v-btn>
  
  </v-card>
</template>

<script setup>
import { postStore } from "@/store/posts.js"
import { userStore } from "@/store/user"

const posts = postStore();
const user = userStore();

</script>

<style>

</style>