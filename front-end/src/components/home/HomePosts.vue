<template>
  <v-card>
    <v-card-title class="font-weight-light"> {{ title }}</v-card-title>
    <v-card-text>
      {{ content }}
    </v-card-text>

    <!-- <div v-if="showComments">
      <v-sheet variant="outlined" class="ma-2 commentCard" border rounded >
          <v-card
            class="pa-0 ma-2"
            variant="tonal"
            density="compact"
            v-for="(comment, idx) in comments"
            :key="idx"
          >
            <v-card-title style="font-size: 1em" class="font-weight-light">
              @{{ comment.username }}</v-card-title
            >
            <v-card-text>{{ comment.comment }}</v-card-text>
          </v-card>
      </v-sheet>
      <div v-if="makeComment">
      <v-textarea
        autofocus
        rows="2"
        class="pl-4 pr-4 pt-2"
        density="compact"
        variant="outlined"
        label="Comment"
        v-model="commentText"
      >
      </v-textarea>
      <div class="pl-2 pr-2 pb-2">
        <v-btn size="small" variant="plain" @click="() => {
          makeComment = false;
          commentText = '';
        }">Cancel</v-btn>
        <v-btn size="small" variant="plain">Send</v-btn>
      </div>
      </div>
    </div> -->

    <v-card-actions>
      <v-btn size="small" icon="mdi-thumb-up"></v-btn>
      <v-btn size="small" icon="mdi-thumb-down"></v-btn>
        <!-- <v-btn
          v-if="showComments"
        
          @click="showComments = false"
     
        ><v-icon>mdi-comment-off</v-icon>({{ comments.length }})</v-btn>
        <v-btn
          v-if="!makeComment && showComments"
          size="small"
          @click="makeComment = true"
          icon="mdi-comment-text"
        ></v-btn> -->
      <v-btn
        @click="()=>{
          router.push(`/posts/${id}`)
        }"
      ><v-icon>mdi-comment</v-icon>(6)</v-btn>
    </v-card-actions>
  </v-card>
</template>
<script setup>
import { ref } from "vue";
import router from "@/router/index.js"

const props = defineProps(["title", "content", "id"]);

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
