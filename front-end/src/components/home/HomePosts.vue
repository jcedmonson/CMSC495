<template>
  <v-card color="primary" variant="tonal">
    <v-card-title class="pb-3 pt-3" style="color: white; font-size: .9em;">
      <v-avatar size="35" variant="elevated" color="primary" class="mb-0 mr-1">{{
        props.post.first_name[0] + props.post.last_name[0]
      }}</v-avatar>

      @{{ props.post.user_name }}</v-card-title
    >
    <v-card-subtitle style="color: white;">{{ props.post.post_date }}</v-card-subtitle>
    <v-card-text style="color: white;">
      {{ props.post.content }}
    </v-card-text>

    <v-card-actions>
      <v-btn size="small" icon="mdi-thumb-up" color="white"></v-btn>
      <v-btn size="small" icon="mdi-thumb-down" color="white"></v-btn>
      <v-btn
        color="white"
        @click="
          () => {
            router.push(`/posts/${props.post.post_id}`);
          }
        "
        ><v-icon>mdi-comment</v-icon>({{ props.post.comments.length }})</v-btn
      >
    </v-card-actions>
  </v-card>
</template>
<script setup>
import { ref } from "vue";
import router from "@/router/index.js";

const props = defineProps(["post"]);

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
