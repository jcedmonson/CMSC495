<template>
  <v-card>
    <v-card-title class="font-weight-light">
      Friends
    </v-card-title>
    <v-card-text v-if="user.connections.length > 0">
      <v-list>
        <v-list-item v-for="(conn, idx) in user.connections" :key="idx"
          :title="`@${conn.username}`"
          :subtitle="`${conn.first_name} ${conn.last_name}`"
        >
        <template v-slot:prepend>
          <v-avatar color="grey">{{ conn.first_name[0] }} {{ conn.last_name[0] }}</v-avatar>
        </template>
        </v-list-item>
      </v-list>
    </v-card-text>
    <v-card-text v-else>
      <v-row>
        <v-col class="text-center">
          You are missing all your friends... <br />
          You should add one!
        </v-col>
      </v-row>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-text>
      <v-row>
        <v-col>
          <v-list density="compact">
            <v-list-item
              v-for="(conn, idx) in app.users.filter((u) => {
                if (u.username != user.username && !user.connections.map((k) => {return k.username}).includes(u.username)){
                  return u;
                }
              })"
              :key="idx"
              :title="`@${conn.username}`"
              :subtitle="`${conn.first_name} ${conn.last_name}`"
              >

              <template v-slot:prepend>
                <v-avatar color="grey">{{ conn.first_name[0] }} {{ conn.last_name[0] }}</v-avatar>
              </template>
              <template v-slot:append>
                <v-btn x-small icon="mdi-account-plus" elevation="0" @click="user.addConnection(conn)"></v-btn>
              </template>

            </v-list-item>
          </v-list>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { userStore } from "@/store/user.js";
import { appStore } from "@/store/app.js";

const user = userStore();
const app = appStore();

app.getUsers();

</script>

<style></style>
