<template>
  <v-snackbar v-model="app.message.show" color="red" location="top">
    <v-row>
      <v-col class="text-center">
        <v-icon icon="mdi-alert" class="mr-1"></v-icon>
        {{ app.message.content }}
      </v-col>
    </v-row>
  </v-snackbar>
</template>
<script setup>
import { appStore } from "@/store/app.js";

const app = appStore();
</script>
