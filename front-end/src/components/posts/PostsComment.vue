<template>
  <v-container class="full-height">
    <v-row>
      <v-col>
        <div style="position: sticky; top: 63px; z-index: 2">
          <v-card elevation="0">
            <v-card-text class="pa-0 ma-0">
              <v-card color="primary" variant="tonal" class="">
                <v-card-title class="font-weight-light" style="color: white">@POSTER</v-card-title>
                <v-card-text style="color: white"
                  >Some random stuff that was said in this post.</v-card-text
                >
              </v-card>
              <v-sheet rounded class="">
                <v-textarea
                  rows="1"
                  class="pl-4 pr-4 mt-2"
                  auto-grow
                  variant="underlined"
                  :label="`Reply to @${title}`"
                >
                </v-textarea>
                <v-btn variant="plain">Send</v-btn>
              </v-sheet>
            </v-card-text>
          </v-card>
        </div>

        <v-card
          variant="tonal"
          color="primary"
          class="mt-3"
          v-for="(comment, idx) in comments"
          :key="idx"
        >
          <v-card-title style="font-size: 0.9em; color: white">
            @{{ comment.username }}
          </v-card-title>
          <v-card-text style="color: white">
            {{ comment.comment }}
          </v-card-text>
        </v-card>
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

const props = defineProps(["title", "content", "id"]);

let comments = [
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
  { username: "lindsay04", comment: "A random comment" },
];
</script>
<style></style>
