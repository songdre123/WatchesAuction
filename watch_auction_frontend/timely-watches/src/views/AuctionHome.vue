<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <v-container>
    <v-tabs v-model="tab" align-tabs="center" color="amber-lighten-2">
      <v-tab v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</v-tab>
    </v-tabs>
      <v-row align="center" justify="center">
        <v-col v-for="(watch, index) in watches[tab]" :key="index" cols="4">
          <WatchCard
            v-if="watch"
            :referenceNo="index"
            :watch="watch"
          />
        </v-col>
      </v-row>
    </v-container>
</template>

<script setup>
  import WatchCard from '@/components/WatchCard.vue'
</script>

<script>
import axios from 'axios'
import { useUserStore } from '@/store/userStore'
const userStore = useUserStore()

  export default {
    data() {
      return {
        categories: ['Rolex', 'Patek Philippe', 'Audemars Piguet'],
        tab: null,
        auctionData: null,
        watches: {
      'Rolex': {
       
      },
      'Patek Philippe': {
       
      },
      'Audemars Piguet': {
        
      }
    }
      }
    },
    computed: {
    watchLength() {
      return this.watches[this.tab] ? this.watches[this.tab].length : 0
    },
  },

   async mounted() {

      try {
        const userResponse = await axios.get(`http://127.0.0.1:5000/user/${userStore.getUser().email}`)
        const userData = userResponse.data.data
        const userID = userData.id
        userStore.setUserId(userID)
        console.log(userID)
      } catch (error) {
        console.error('Error getting user:', error.message);
        throw error; // Re-throw the error to propagate it further
      }

      this.tab = this.categories[0]; // Initialize tab to the first category
      try {
        const response = await axios.get('http://127.0.0.1:5001/auction')
        console.log(response.data.data.auctions)
        this.auctionData = response.data.data.auctions;
        for (let i = 0; i < this.auctionData.length; i++) {
        console.log(this.auctionData[i])
        if (this.auctionData[i].watch_brand == 'Rolex') {
          this.watches['Rolex'][this.auctionData[i].watch_ref] = {
            'auctionID' : this.auctionData[i].auction_id,
            'title' : this.auctionData[i].auction_item,
            'StartDate' : this.auctionData[i].start_time,
            'EndDate' : this.auctionData[i].end_time,
            'MinBid' : this.auctionData[i].start_price,
            'CurrentPrice' : this.auctionData[i].current_price,
            'WatchBoxPresent' : this.auctionData[i].watch_box_present,
            'WatchPapersPresent' : this.auctionData[i].watch_papers_present,
            'Condition' : this.auctionData[i].watch_condition,
            'AuctionWinner' : this.auctionData[i].auction_winner_id,
            'AuctionStatus' : this.auctionData[i].auction_status,
            'ImageList' : [this.auctionData[i].watch_image1, this.auctionData[i].watch_image2, this.auctionData[i].watch_image3],
            'imageURL' : this.auctionData[i].watch_image1 
          }
        }
        else if (this.auctionData[i].watch_brand == 'Patek Philippe') {
          this.watches['Patek Philippe'][this.auctionData[i].watch_ref] = {
            'auctionID' : this.auctionData[i].auction_id,
            'title' : this.auctionData[i].auction_item,
            'StartDate' : this.auctionData[i].start_time,
            'EndDate' : this.auctionData[i].end_time,
            'MinBid' : this.auctionData[i].start_price,
            'CurrentPrice' : this.auctionData[i].current_price,
            'WatchBoxPresent' : this.auctionData[i].watch_box_present,
            'WatchPapersPresent' : this.auctionData[i].watch_papers_present,
            'Condition' : this.auctionData[i].watch_condition,
            'AuctionWinner' : this.auctionData[i].auction_winner_id,
            'AuctionStatus' : this.auctionData[i].auction_status,
            'ImageList' : [this.auctionData[i].watch_image1, this.auctionData[i].watch_image2, this.auctionData[i].watch_image3],
            'imageURL' : this.auctionData[i].watch_image1 
          }
        }
        else {
          this.watches['Audemars Piguet'][this.auctionData[i].watch_ref] = {
            'auctionID' : this.auctionData[i].auction_id,
            'title' : this.auctionData[i].auction_item,
            'StartDate' : this.auctionData[i].start_time,
            'EndDate' : this.auctionData[i].end_time,
            'MinBid' : this.auctionData[i].start_price,
            'CurrentPrice' : this.auctionData[i].current_price,
            'WatchBoxPresent' : this.auctionData[i].watch_box_present,
            'WatchPapersPresent' : this.auctionData[i].watch_papers_present,
            'Condition' : this.auctionData[i].watch_condition,
            'AuctionWinner' : this.auctionData[i].auction_winner_id,
            'AuctionStatus' : this.auctionData[i].auction_status,
            'ImageList' : [this.auctionData[i].watch_image1, this.auctionData[i].watch_image2, this.auctionData[i].watch_image3],
            'imageURL' : this.auctionData[i].watch_image1 
          }
        }
    }
      }
      catch (error) {
        console.error('Error fetching auction data', error.message)
      }
      
    },
}
</script>

