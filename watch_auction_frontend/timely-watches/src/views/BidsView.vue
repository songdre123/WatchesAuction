<template>

    <v-container>
        <v-row dense>
            <v-col cols="12">
                <v-card elevation="4" v-for="bid in highestBids" :key="bid" color="brown-lighten-4" theme="dark">
                    <div class="d-flex justify-space-between">
                        <div>
                            <v-card-title class="text-h5">Auction Name : {{ bid.title }} {{ bid.ref_number }} </v-card-title>
            
                            <v-card-title >Auction ID : {{ bid.auctionID }} </v-card-title>

                            <v-card-subtitle>Your Current Bid Amount : $SGD {{ bid.bid_amount }}</v-card-subtitle>

                            <v-card-actions>
                                <v-btn @click="selectBid(bid)" class="ms-2 mr-2" size="small" variant="outlined">
                                    Enter bid
                                </v-btn>
                            </v-card-actions>
                        </div>

                        <v-avatar class="ma-3" rounded="0" size="125">
                            <v-img
                            :src="bid.imageURL"
                            ></v-img>
                        </v-avatar>
                    </div>

                </v-card>
            </v-col>
        </v-row>
    </v-container>


</template>

<script>
import { useWatchStore } from '@/store/watchStore'
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/userStore'
import axios from 'axios'

const watchStore = useWatchStore()
const userStore = useUserStore()


export default {
    setup() {
        const highestBids = ref([])
        const selectedBid = ref(null);
        const router = useRouter()
        // const watchId = computed(() => route.params.id)

        onMounted(async () => {
            const userId = computed(() => userStore.userID)
            try {
                const userResponse = await axios.get(`http://127.0.0.1:5002/bid/user/${userId.value}`)
                const data = userResponse.data.data
                const groupedBids = data.reduce((acc, bid) => {
                    if (!acc[bid.auction_id] || acc[bid.auction_id].bid_amount < bid.bid_amount) {
                        acc[bid.auction_id] = bid;
                    }
                    return acc
                }, {})
                highestBids.value = Object.values(groupedBids);
                console.log(highestBids.value)

                for (let bid of highestBids.value) {
                    try {
                        const auctionResponse = await axios.get(`http://127.0.0.1:5001/auction/${bid.auction_id}`)
                        const auctionData = auctionResponse.data.data

                        bid.auctionID = bid.auction_id; // Rename auction_id to auctionID
                        delete bid.auction_id; // Remove old key
                        bid.title = auctionData.auction_item;
                        bid.imageURL = auctionData.watch_image1;
                        bid.ref_number = auctionData.watch_ref
                        bid.watch_brand = auctionData.watch_brand;
                        bid.manufactureYear = auctionData.manufacture_year;
                        bid.StartDate = auctionData.start_time;
                        bid.EndDate = auctionData.end_time;
                        bid.MinBid = auctionData.start_price;
                        bid.CurrentPrice = auctionData.current_price;
                        bid.WatchBoxPresent = auctionData.watch_box_present;
                        bid.WatchPapersPresent = auctionData.watch_papers_present;
                        bid.Condition = auctionData.watch_condition;
                        bid.AuctionWinner = auctionData.auction_winner_id;
                        bid.AuctionStatus = auctionData.auction_status;
                        bid.ImageList = [auctionData.watch_image1, auctionData.watch_image2, auctionData.watch_image3]

                        console.log(auctionData)
                    } catch (error) {
                        console.error(`Error Message`, error.message)
                        console.log(error.status)
                    }
                }
            } catch (error) {
                console.error(`Error Message`, error.message)
                console.log(error.status)
            }
        });

        const selectBid = (bid) => {
            selectedBid.value = bid;
            const watchDetails = {
                'auctionID' : bid.auctionID,
                'title' : bid.title,
                'manufactureYear' : bid.manufactureYear,
                'StartDate' : bid.StartDate,
                'EndDate' : bid.EndDate,
                'MinBid' : bid.MinBid,
                'CurrentPrice' : bid.CurrentPrice,
                'WatchBoxPresent' : bid.WatchBoxPresent,
                'WatchPapersPresent' : bid.WatchPapersPresent,
                'Condition' : bid.Condition,
                'AuctionWinner' : bid.AuctionWinner,
                'AuctionStatus' : bid.AuctionStatus,
                'ImageList' : bid.ImageList,
                'imageURL' : bid.imageURL,
            }

            watchStore.setWatch(watchDetails)
            router.push({name: 'AuctionDetails', 
                params: {id : bid.ref_number},
            })
        }
        return { highestBids, selectBid };
    }
}



</script>