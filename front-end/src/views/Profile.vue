<template>
  <v-container>
    <v-row>
      <v-col class="d-none d-md-block"> </v-col>
      <v-col xs="12" sm="12" md="6" lg="6" xl="4">
        <v-card>
          <v-card-title class="font-weight-light pb-3 pt-3">
            <v-avatar
              size="35"
              variant="elevated"
              color="primary"
              class="mr-1"
              >{{ user.first_name[0] + user.last_name[0] }}</v-avatar
            >

            @{{ user.user_name }}</v-card-title
          >
          <v-divider></v-divider>
          <v-card-text>
            <v-list>
              <v-list-item>
                <v-list-item-title>First Name<v-list-item-subtitle>{{user.first_name}}</v-list-item-subtitle></v-list-item-title>
              </v-list-item>
                            <v-list-item>
                <v-list-item-title>Last Name<v-list-item-subtitle>{{user.last_name}}</v-list-item-subtitle></v-list-item-title>
              </v-list-item>
                            <v-list-item>
                <v-list-item-title>Email<v-list-item-subtitle>{{user.email}}</v-list-item-subtitle></v-list-item-title>
              </v-list-item>
                            <v-list-item>
                <v-list-item-title>Connections<v-list-item-subtitle>{{connections.connections.length}}</v-list-item-subtitle></v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col class="d-none d-md-block"></v-col>
    </v-row>
  </v-container>
</template>
<script setup>
import { userStore } from "@/store/user";
import { connectionsStore } from "@/store/connections";

const user = userStore();
const connections = connectionsStore();
</script>
<style></style>
