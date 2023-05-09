<template>
  <v-container class="full-height" fluid>
    <v-row>
      <v-col class="d-none d-md-block"> </v-col>
      <v-col xs="12" sm="12" md="6" lg="6" xl="4">
        <posts-comment
        ></posts-comment>
      </v-col>
      <v-col class="d-none d-md-block"></v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { postStore } from "@/store/posts";
import router from "@/router/index.js";
import PostsComment from "@/components/posts/PostsComment.vue";

const posts = postStore();

</script>

<style scoped></style>
