<template>
  <v-container class="fill-height loginBackground" fluid>
    <v-row>
      <v-col xs=2 sm=4 md=4 lg=4 xl=5></v-col>
      <v-col xs=8 sm=6 md=6 lg=4 xl=2> <LoginCard class="mb-3" /></v-col>
      <v-col xs=2 sm=4 md=4 lg=4 xl=5></v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import LoginCard from "@/components/LoginCard.vue";
</script>

<style scoped>

.loginBackground{
  background: rgb(1,130,255);
  background: radial-gradient(circle, #0182ff 0%, rgba(38,50,56,1) 100%);
}

</style>
