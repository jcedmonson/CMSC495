<template>
  <v-card :color="props.post.user_id == user.user_id ? 'indigo': 'indigo-lighten-2'" variant="tonal">
    <v-card-title class="pb-3 pt-3" style="color: white; font-size: 0.9em">
      <v-avatar
        size="35"
        variant="elevated"
        color="primary"
        class="mb-0 mr-1"
        >{{ props.post.first_name[0] + props.post.last_name[0] }}</v-avatar
      >

      @{{ props.post.user_name }}</v-card-title
    >
    <v-card-subtitle style="color: white">{{
      props.post.post_date
    }}</v-card-subtitle>
    <v-card-text style="color: white">
      {{ props.post.content }}
    </v-card-text>
    <v-card-actions>
      <v-btn
        size="small"
        color="white"
        @click="posts.postReaction(props.post.post_id, 1)"
        ><v-icon icon="mdi-thumb-up" class="mr-1"></v-icon>
        <div v-if="reactions.likes > 0">{{ reactions.likes }}</div></v-btn
      >
      <v-btn
        size="small"
        color="white"
        @click="posts.postReaction(props.post.post_id, 2)"
        ><v-icon icon="mdi-thumb-down" class="mr-1"></v-icon>
        <div v-if="reactions.dislikes > 0">{{ reactions.dislikes }}</div></v-btn
      >
      <v-btn
        color="white"
        @click="
          () => {
            posts
              .viewPost(props.post.post_id)
              .then(() => {
                router.push(`/posts/${props.post.post_id}`);
              })
              .catch((err) => {
                app.showMessage(err);
              });
          }
        "
        ><v-icon class="mr-1">mdi-comment</v-icon>
        <div v-if="props.post.comments.length > 0">
          {{ props.post.comments.length }}
        </div></v-btn
      >
      <v-spacer></v-spacer>
      <v-btn color="white" v-if="props.post.user_id == user.user_id" @click="posts.deletePost(props.post.post_id)"><v-icon icon="mdi-delete"></v-icon></v-btn>
    </v-card-actions>
  </v-card>
</template>
<script setup>
import { computed, ref } from "vue";
import router from "@/router/index.js";
import { postStore } from "@/store/posts";
import { appStore } from "@/store/app.js";
import { userStore } from "@/store/user.js"

const posts = postStore();
const app = appStore();
const user = userStore();

const props = defineProps(["post"]);

const reactions = computed(() => {
  let likes = 0;
  let dislikes = 0;
  props.post.reactions.forEach((r) => {
    switch (r.reaction_id) {
      case 1:
        likes = likes + 1;
        break;
      case 2:
        dislikes = dislikes + 1;
        break;
    }
  });
  return { likes: likes, dislikes: dislikes };
});

// let showComments = ref(false);
// let makeComment = ref(false);
// let commentText = "";
</script>
<style>
.commentCard {
  max-height: 25vh;
  overflow-y: auto;
}
</style>
