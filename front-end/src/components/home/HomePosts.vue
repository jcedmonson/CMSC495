<template>
  <v-card>
    <v-card-title class="font-weight-light"> {{ title }}</v-card-title>
    <v-card-text>
      {{ content }}
    </v-card-text>
    <v-card-actions>
      <v-btn size="small" icon="mdi-thumb-up"></v-btn>
      <v-btn size="small" icon="mdi-thumb-down"></v-btn>
    </v-card-actions>
  </v-card>
</template>
<script setup>
  const props = defineProps(['title', 'content'])
</script>
<style>
</style>