<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="layout">
    <h1 class="header">Timely Watches</h1>
    <SignUpForm class="form" />
  </div>
</template>

<script setup>
import SignUpForm from '@/components/SignUpForm.vue';
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