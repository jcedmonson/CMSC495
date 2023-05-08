<template>
  <v-container class="login fill-height loginBackground" fluid>
    <v-row>
      <v-col class="d-none d-md-block"></v-col>
      <v-col lg="4" xl="3">
        <LoginCard
      /></v-col>
      <v-col class="d-none d-md-block"></v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import LoginCard from "@/components/login/LoginCard.vue";
</script>

<style scoped>
.loginBackground {
  background: radial-gradient(circle, #5c6bc0 0%, rgba(38, 50, 56, 1) 100%);
}



/* .loginBackground{
  background: #3F51B5;
} */
</style>
