<template>
  <v-container class="full-height">
    <v-row>
      <v-col>
        <div style="position: sticky; top: 63px; z-index: 2">
          <v-card elevation="0">
            <v-card-text class="pa-0 ma-0">
              <v-card elevation="0">

                <v-card-title class="font-weight-light pb-3 pt-3">
                  <v-avatar size="35" variant="elevated" color="primary" class="mr-1">{{
                    posts.selectedPost.first_name[0] + posts.selectedPost.last_name[0]
                  }}</v-avatar>

                  @{{ posts.selectedPost.user_name }}</v-card-title
                >


                <v-card-text style="color: white" class="mt-2"
                  >{{posts.selectedPost.content}}</v-card-text
                >
              </v-card>
              <v-card rounded color="primary" class="mt-2" elevation="0">
                <v-textarea
                  rows="1"
                  class="pl-4 pr-4 pt-1"
                  auto-grow
                  variant="underlined"
                  :label="`Reply to @${posts.selectedPost.user_name}`"
                  v-model="posts.comment"
                >
                </v-textarea>
                <v-btn variant="plain" @click="posts.postComment()">Send</v-btn>
              </v-card>
            </v-card-text>
          </v-card>
        </div>

        <div v-if="posts.selectedPost.comments.length > 0">
                  <v-card
          
          variant="tonal"
          color="primary"
          class="mt-3"
          v-for="(comment, idx) in posts.selectedPost.comments"
          :key="idx"
        >
          <v-card-title style="font-size: 0.9em; color: white">
            @{{ comment.username }}
          </v-card-title>
          <v-card-text style="color: white">
            {{ comment.comment }}
          </v-card-text>
        </v-card>
        </div>
        <div v-else>
                            <v-card
          
          variant="tonal"
          color="primary"
          class="mt-3"
        >
          <v-card-text style="color: white" class="text-center">
            This post does not have any comments.
          </v-card-text>
        </v-card>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col> </v-col>
    </v-row>
  </v-container>
</template>
<script setup>
import { ref } from "vue";
import router from "@/router/index.js";
import { postStore } from "@/store/posts";
const posts = postStore();


// const props = defineProps(["title", "content", "id"]);

</script>
<style></style>
