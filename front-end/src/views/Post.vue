<template>
  <v-container class="full-height" fluid>
    <v-row class="full-height">
      <v-col></v-col>
      <v-col md="6" lg="4">
        <posts-comment
         
          :title="posts.selectedPost.username"
          :content="posts.selectedPost.content"
          :id="posts.selectedPost.postId"
        ></posts-comment>
      </v-col>
      <v-col></v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { postStore } from "@/store/posts";
import router from "@/router/index.js";
import PostsComment from "@/components/posts/PostsComment.vue";

const posts = postStore();
posts.viewPost(router.currentRoute.value.params.id);
</script>

<style scoped></style>
