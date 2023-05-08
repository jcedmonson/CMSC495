<template>
  <v-container>
    <v-row>
      <v-col></v-col>
      <v-col md="6" lg="6" xl="6">
        <v-card>
          <v-card-text>
            <v-text-field label="User Search"></v-text-field>
            <v-list>
              <v-list-item v-for="(u, idx) in connections.users" :key="idx">
                <template v-slot:prepend>
                  <v-avatar variant="elevated" color="primary">{{
                    u.first_name[0] + u.last_name[0]
                  }}</v-avatar>
                </template>
                <v-list-item-title><h4>@{{u.user_name}}</h4></v-list-item-title>
                <template v-slot:append>
                  <v-btn variant="text"><v-icon icon="mdi-plus"></v-icon>Add</v-btn>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col></v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { connectionsStore } from "@/store/connections.js";

const connections = connectionsStore();

connections.getUsers();
</script>

<style></style>
