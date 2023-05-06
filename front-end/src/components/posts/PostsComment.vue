<template>
  <v-container class="full-height">
    <v-row>
      <v-col>
        <v-sheet class="pb-2" rounded>
          <div style="position: sticky; top: 63px; z-index: 2;">
            <v-card elevation="0">
              <v-card-title class="font-weight-light mt-2">
                @{{ title }}</v-card-title
              >
              <v-card-text>
                {{ content }}
                <v-sheet border rounded class="mt-5">
                  <v-textarea
                    rows="1"
                    class="pl-3 pr-3 mt-2"
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
     
          <v-card variant="tonal" class="ma-4" v-for="(comment, idx) in comments" :key="idx">
            <v-card-title style="font-size: .9em;">
              @{{ comment.username }}
            </v-card-title>
            <v-card-text>
              {{ comment.comment }}
            </v-card-text>
          </v-card>
        </v-sheet>
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
