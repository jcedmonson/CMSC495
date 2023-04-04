<template>
  <v-container class="" fluid>
    <v-app-bar title="CityPark">
      <template v-slot:prepend>
        <v-app-bar-nav-icon></v-app-bar-nav-icon>
      </template>
      <v-avatar>{{ user.first_name[0]+user.last_name[0] }}</v-avatar>
    </v-app-bar>
    <v-container>
      <v-row>
        <v-col  xs="12" sm="4" md="4" lg="4" xl="4">
          <home-friends style="max-width: 400px"></home-friends>
        </v-col>
        <v-col xs="12" sm="6" md="6" lg="6" xl="4">
          <home-create-post class="ml-5 mr-5 mb-5"></home-create-post>
          <home-posts
            class="ml-5 mr-5 mb-5"
            v-for="(post, idx) in posts.currentPosts"
            :key="idx"
            :title="'@'+post.username"
            :content="post.content"
          ></home-posts>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script setup>
import { userStore } from "@/store/user";
import { postStore } from "@/store/posts";

import HomePosts from "@/components/home/HomePosts.vue";
import HomeCreatePost from "@/components/home/HomeCreatePost.vue";
import HomeFriends from "@/components/home/HomeFriends.vue";

const user = userStore();
const posts = postStore();
posts.getPosts();
</script>

<style scoped>
</style>
