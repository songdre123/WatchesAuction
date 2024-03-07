<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <v-app class="background">
        <v-layout class="layout">
        <h1 class="header">
            <svg-icon type="mdi" :path="path"></svg-icon>
            Timely Watches
        </h1>
        <!-- <v-divider class="divider" color="black" length="300px"></v-divider> -->
        <SignUpForm class="form"/>
        </v-layout>
    </v-app>
</template>

<script setup>
    import SignUpForm from '@/components/SignUpForm.vue';
    import SvgIcon from '@jamescoyle/vue-icon';
    import { mdiWatch } from '@mdi/js';
</script>

<script>
export default {
    data() {
        return {
            path: mdiWatch
        }   
    },
}
</script>

<style scoped>

@font-face {
  font-family: Riviera Nights;
  src: url(@/styles/rivieraNights/RivieraNights.otf)
}

.layout {
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content:center;
    align-items: center;
}

.header {
    font-family:Riviera Nights;
    font-size: 36px;
    text-align: center;
    margin-top: 20px;
}

.form {
    margin-bottom: 20px;
}

.background{
background-image: linear-gradient(to bottom, rgba(255, 187, 51, 0.8), rgba(121, 52, 0, 0.8));
  background-size: cover;
  background-repeat: no-repeat;
  height: 100vh; /* Adjust height as needed */
  width: 100vw; /* Adjust width as needed */
  position: relative;
}
</style>