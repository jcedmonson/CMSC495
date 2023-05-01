<template>
    <v-snackbar v-model="app.message.show" location="top">
        {{app.message.content}}
    </v-snackbar>    
</template>
<script setup>
import { appStore } from "@/store/app.js"

const app = appStore();

</script>