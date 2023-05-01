<template>
  <v-card class="pa-3" style="max-width: 500px;">
    <v-card-title>
      <h3 class="font-weight-light mb-3" v-if="!newUser"> <v-icon icon="mdi-city" class="mb-1"></v-icon>CityPark</h3>
      <h3 class="font-weight-light mb-3" v-else> <v-icon icon="mdi-account-plus" class="mb-1"></v-icon> Account Creation</h3>
    </v-card-title>
    <v-card-text v-if="user.newUser">Please enter the required information to join.</v-card-text>
    <v-form class="pl-2 pr-2" v-if="!user.newUser">
      <v-text-field
        variant="outlined"
        label="Username"
        v-model="user.user_name"
      ></v-text-field>
      <v-text-field
        variant="outlined"
        type="password"
        label="Password"
        v-model="user.password"
      ></v-text-field>
      <v-btn :loading="user.loading" block color="primary" prepend-icon="mdi-login" @click="user.login">Login</v-btn>
      <v-btn class="mt-3" block color="secondary" prepend-icon="mdi-account-plus" @click="user.newUser = true"
        >Sign Up</v-btn
      >
    </v-form>
    <v-form class="pl-2 pr-2" v-else>
      <v-text-field
        variant="outlined"
        label="First Name"
        v-model="user.first_name"
      ></v-text-field>
      <v-text-field
        variant="outlined"
        label="Last Name"
        v-model="user.last_name"
      ></v-text-field>
      <v-text-field
        variant="outlined"
        label="Email"
        v-model="user.email"
      ></v-text-field>
      <v-text-field
        variant="outlined"
        label="Username"
        v-model="user.user_name"
      ></v-text-field>
      <v-text-field
        variant="outlined"
        type="password"
        label="Password"
        v-model="user.password"
      ></v-text-field>
      <v-btn block color="primary" :loading="user.loading" @click="user.createUser">Join</v-btn>
    </v-form>
  </v-card>
</template>

<script setup>
import { ref } from "vue";
import { userStore } from "@/store/user";

let newUser = ref(false)

const user = userStore();
</script>

<style></style>
