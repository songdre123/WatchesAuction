<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <v-container>
      <v-row align="center" justify="center">
        <v-col v-for="i in 6" :key="i" cols="4">
          <WatchCard />
        </v-col>
      </v-row>
    </v-container>
</template>

<script setup>
  import WatchCard from '@/components/WatchCard.vue'
</script>
