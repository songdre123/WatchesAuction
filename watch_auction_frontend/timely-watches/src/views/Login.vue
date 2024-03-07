<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <v-app>
        <SignUpForm />
        <router-view />
    </v-app>
</template>

<script setup>
    import SignUpForm from '@/components/SignUpForm.vue';
</script>
