<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <!-- Include profile picture and allow user to upload image -->
    <div>
        <ProfilePictureUpload />
        <Settings />
    </div>

</template>




<script setup>
import ProfilePictureUpload from "@/components/ProfileUpload.vue";
import Settings from "@/components/ProfileSettings.vue"
</script>

<style scoped>

@font-face {
  font-family: Riviera Nights;
  src: url(@/styles/rivieraNights/RivieraNights-Regular.otf)
}

.text {
  font-family: Riviera Nights, sans-serif;
  font-style: italic;
}


</style>
