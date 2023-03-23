<template>
  <v-container class="fill-height appBackground" fluid>
    <v-app-bar title="App Name Here">
      <template v-slot:prepend>
          <v-app-bar-nav-icon></v-app-bar-nav-icon>
        </template>
        <v-avatar>SU</v-avatar>
    </v-app-bar>
  </v-container>
</template>

<script setup>
import { userData } from '@/store/user'

const user = userData();
</script>

<style scoped>
.appBackground{
  background: rgb(1,130,255);
  background: radial-gradient(circle, #0182ff 0%, rgba(38,50,56,1) 100%);
}
</style>
