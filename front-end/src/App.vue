<template>
  <router-view />
</template>

<script setup>
console.log(process.env.AUTH_SERVICE)
</script>

<style>
.full-height{
  height: 100%;
}

.half-height{
  height: 50%;
}
</style>