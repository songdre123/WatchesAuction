<template>
    <v-layout class="d-flex justify-space-between">
        <v-container>
            <v-row>
                <v-col cols="6" ml="3">
                    <v-img :src="watch.imageURL"></v-img>
                </v-col>
                <v-col cols="6">
                    <div>
                        <v-sheet border="md" class="pa-6 mx-auto" color="amber-lighten-5" max-width="500" :style="{ fontFamily: 'Riviera Nights', minHeight: '500px' }">
                            <h2 class="sheet-title">Watch Name: {{ watch.title }}</h2>
                            <v-divider class="mt-3 mb-3"></v-divider>
                            
                            <span class="d-flex justify-space-between">
                                <h5 class="mb-3">Start Date of Auction: <u>{{ watch.StartDate }}</u></h5>

                                
                                <v-dialog max-width="500">
                                    <template v-slot:activator="{ props: activatorProps }">
                                        <v-btn v-bind="activatorProps" class="mb-2 mr-2" rounded :disabled="!isBidEnabled">Bid</v-btn>
                                    </template>
                                    <template v-slot:default="{ isActive }">
                                        <v-card title="Confirm Bid of Amount">
                                            <v-card-text>
                                                Please confirm that you are willing and able to make a total bid of $SGD {{ watch.MinBid }}
                                            </v-card-text>

                                            <v-card-subtitle class="text-white-50" style="white-space: normal;">
                                                Disclaimer: Down Payment of 10% of the Watch Winning Bid must
                                                be made before full payment and claim of watch
                                            </v-card-subtitle>

                                            <v-card-actions>
                                            <v-spacer></v-spacer>
                                            <v-btn
                                                text="Close"
                                                @click="isActive.value = false"
                                            ></v-btn>
                                            <v-btn 
                                                text="Make Bid" 
                                                @click="isActive.value = false"
                                            ></v-btn>
                                            </v-card-actions>
                                        </v-card>
                                    </template>
                                </v-dialog>
                            </span>
                            <h5 class="mb-3">End Date of Auction: <u>{{ watch.EndDate }}</u></h5>

                            <v-divider class="mt-3 mb-3"></v-divider>

                            <h5 class="mb-3">Current Bid: {{ watch.MinBid }} SGD</h5>
                            <h5 class="mb-3">Minimum Bid: {{ watch.MinBid }} SGD</h5>
                            <p class="mb-3">Watch Condition: {{ watch.Condition }}</p>
                            <p class="mb-3">Watch Box Present: {{ isWatchBoxPresent }}</p>
                            <p class="mb-3">Watch Papers Present: {{ isWatchPapersPresent }}</p>
                            
                            <p class="mb-3">Watch Status: In Progress</p>

                        </v-sheet>
                    </div>
                </v-col>
            </v-row>
        </v-container>
    </v-layout>
</template>


<script>
import { useWatchStore } from '@/store/watchStore'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

export default {
    setup() {
        const watchStore = useWatchStore()
        const watch = computed(() => watchStore.getWatch())

        const route = useRoute()
        const id = computed(() => route.params.id)

        const isBidEnabled = computed(() => {
            const watchStartDate = new Date(watch.value.StartDate)
            const watchEndDate = new Date(watch.value.EndDate)

             // 2 hours in milliseconds
            const currentDate = new Date()

            return currentDate >= watchStartDate && currentDate <= watchEndDate
        })

        const isWatchBoxPresent = computed(() => {
            const watchBoxPresent = watch.value.WatchBoxPresent
            return watchBoxPresent ? 'Present' : 'Not Present'
        })

        const isWatchPapersPresent = computed(() => {
            const watchPapersPresent = watch.value.WatchPapersPresent
            return watchPapersPresent ? 'Present' : 'Not Present'
        })

        return { watch, id, isBidEnabled, isWatchBoxPresent, isWatchPapersPresent}
    }
}
;
</script>

<style scoped>
@font-face {
  font-family: Riviera Nights;
  src: url(@/styles/rivieraNights/RivieraNights-Regular.otf)
}

.sheet-title {
  font-family: Riviera Nights, sans-serif;
  font-style: oblique;
}

p {
    font-size: 14px;
}

</style>