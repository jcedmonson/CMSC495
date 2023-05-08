<template>
  <v-container>
    <v-row>
      <v-col class="d-none d-md-block"> </v-col>
      <v-col xs="12" sm="12" md="6" lg="6" xl="4">
        <v-card>
          <v-card-text class="ma-0 pa-0">
            <v-text-field label="User Search" v-model="search" @update:modelValue="searchUser"></v-text-field>
            <v-list class="mb-4">
              <v-list-item v-for="(u, idx) in possibleConnections" :key="idx">
                <template v-slot:prepend>
                  <v-avatar variant="elevated" color="primary">{{
                    u.first_name[0] + u.last_name[0]
                  }}</v-avatar>
                </template>
                <v-list-item-title
                  ><h4>@{{ u.user_name }}</h4></v-list-item-title
                >
                <template v-slot:append>
                  <v-btn
                    v-if="!connectionIds.includes(u.user_id)"
                    variant="text"
                    @click="connections.addConnection(u)"
                    ><v-icon icon="mdi-plus"></v-icon>Add</v-btn
                  >
                  <v-icon v-else icon="mdi-check" color="green"></v-icon>
                </template>
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
import { connectionsStore } from "@/store/connections.js";
import { userStore } from "@/store/user.js";
import { computed, ref } from "vue";

const connections = connectionsStore();
const user = userStore();

const connectionIds = computed(() => {
  return connections.connections.map((u) => {
    return u.user_id;
  });
});
const possibleConnections = computed(() => {
  return connections.users.filter((u) => {
    return u.user_id != user.user_id;
  });
});

connections.getUsers();
connections.getConnections();

const search = ref('')

const searchUser = (v) => {
  setTimeout(() => {
    if (v.length == 0){
      connections.getUsers();
    } else if (v == search.value) {
      connections.searchUsers(v);
    }
  }, 1000)
}


</script>

<style></style>
