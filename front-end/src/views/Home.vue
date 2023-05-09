<template>
  <v-container v-if="!loading" class="" fluid>
    <v-row v-if="connections.connections.length == 0">
      <v-col class="d-none d-md-block"> </v-col>
      <v-col xs="12" sm="12" md="6" lg="6" xl="4">
        <v-alert
          @click="router.push({ name: 'Connections' })"
          class="ml-5 mr-5 font-weight-light"
          title="Missing Connections"
          type="warning"
          density="compact"
          variant="tonal"
          text="You are not connected with anyone! This means that you will not be able to see posts from other people. You can search for and add a connection by navigating to the connections page via the navigation drawer."
        >
        </v-alert>
      </v-col>
      <v-col class="d-none d-md-block"></v-col>
    </v-row>
    <v-row>
      <v-col class="d-none d-md-block"> </v-col>
      <v-col xs="12" sm="12" md="6" lg="6" xl="4">
        <home-create-post
          class="ml-5 mr-5 mb-5"
          style="position: sticky; top: 63px; z-index: 2"
        ></home-create-post>
        <home-posts
          class="ml-5 mr-5 mb-5"
          v-for="(post, idx) in posts.currentPosts"
          :key="idx"
          :post="post"
        ></home-posts>
      </v-col>
      <v-col class="d-none d-md-block"></v-col>
    </v-row>
  </v-container>
  <v-container v-else class="fill-height" fluid>
    <v-row
      ><v-col class="text-center mb-15"
        ><v-progress-circular
          indeterminate
          size="50"
        ></v-progress-circular></v-col
    ></v-row>
  </v-container>
</template>

<script setup>
import { userStore } from "@/store/user";
import { postStore } from "@/store/posts";
import { connectionsStore } from "@/store/connections";
import router from "@/router";

import HomePosts from "@/components/home/HomePosts.vue";
import HomeCreatePost from "@/components/home/HomeCreatePost.vue";
import HomeFriends from "@/components/home/HomeFriends.vue";
import { ref } from "vue";

let loading = ref(true);

const user = userStore();
const posts = postStore();
const connections = connectionsStore();

posts.getPosts();
connections.getConnections();

Promise.all([posts.getPosts(), connections.getConnections()]).then((resp) => {
  loading.value = false;
});
</script>
<style scoped></style>
