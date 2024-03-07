<template>
    <v-hover v-slot="{isHovering, props}">
    <v-card class="mx-auto" max-width="400" v-bind="props">
        <v-img
            src="https://cdn.watchbase.com/watch/lg/origin:png/rolex/datejust-31/278341rbr-0023-f.webp"
            height="200px"
            cover>
        </v-img>
        <v-card-title class="title">
            Rolex Watch
        </v-card-title>
        <v-card-subtitle class="content">
            <b>Ref</b>: 156940390z
        </v-card-subtitle>
        <v-card-text class="content">
            Date: 24/03 16:00 GMT
        </v-card-text>
        <v-card-text class="content">
            Opening: $80000 SGD
        </v-card-text>

        <v-overlay :model-value="isHovering" class="align-center justify-center" contained>
            <v-btn class="content">Enter Auction</v-btn>
        </v-overlay>

    </v-card>
    </v-hover>
</template>

<script>
    // export default {
    //     props: ['img_src', 'card_titles', '']
    // }
</script>

<style scoped>

@font-face {
  font-family: Riviera Nights;
  src: url(@/styles/rivieraNights/RivieraNights-Regular.otf);
}

@font-face {
    font-family: Riviera Nights dark;
    src: url(@/styles/rivieraNights/RivieraNights-Black.otf)
}

.title {
    font-family: Riviera Nights dark, sans-serif
}

.content {
    font-family: Riviera Nights, sans-serif
}

</style>
