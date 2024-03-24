<template>
    <v-hover v-slot="{isHovering, props}">
    <v-card class="mx-auto" max-width="400" v-bind="props" @click="goToWatchDetails">
        <v-img
            :src="watch.imageURL"
            height="200px"
            cover>
        </v-img>
        <v-card-title class="title">
            {{ watch.title }}
        </v-card-title>
        <v-card-subtitle class="content">
            <b>Ref</b>: {{ referenceNo }}
        </v-card-subtitle>
        <v-card-text class="content">
            Date: {{ watch.StartDate }}
        </v-card-text>
        <v-card-text class="content">
            Opening: ${{ watch.MinBid }} SGD
        </v-card-text>

        <v-overlay :model-value="isHovering" class="align-center justify-center" contained>
            <v-btn class="content">Enter Auction</v-btn>
        </v-overlay>

    </v-card>
    </v-hover>
</template>

<script>

import { useWatchStore } from '@/store/watchStore'
const watchStore = useWatchStore()

    export default {
        props: ['referenceNo', 'watch'],
        methods: {
            goToWatchDetails() {
                watchStore.setWatch(this.watch)
                this.$router.push({name: 'AuctionDetails', 
                params: {id : this.referenceNo},
            })
            }
        }
        
           
}
    
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
