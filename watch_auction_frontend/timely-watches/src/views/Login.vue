<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
  <div class="layout">
    <h1 class="header">Timely Watches</h1>
    <v-btn @click="toggleRegister">Toggle Form</v-btn>
    <SignUpForm v-if="isRegister" class="form" />
    <LoginForm v-else class="form" />
  </div>
  </v-app>
</template>

<script setup>
import SignUpForm from '@/components/SignUpForm.vue';
import LoginForm from '@/components/LoginForm.vue';

</script>

<script>
export default {
  data() {
    return {
      isRegister : true,
    }
  },
  methods: {
    toggleRegister() {
      this.isRegister = !this.isRegister
    }
  }
}
</script>

<style scoped>
@font-face {
  font-family: Riviera Nights;
  src: url(@/styles/rivieraNights/RivieraNights.otf)
}

html, body, .layout {
  height: 100%;
}

.layout {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-image: linear-gradient(to bottom, rgba(255, 187, 51, 0.8), rgba(121, 52, 0, 0.8));
  background-size: cover;
  background-repeat: no-repeat;
}

.header {
  font-family: Riviera Nights;
  font-size: 36px;
  text-align: center;
  margin-top: 20px;
}

.form {
  margin-bottom: 20px;
}

</style>