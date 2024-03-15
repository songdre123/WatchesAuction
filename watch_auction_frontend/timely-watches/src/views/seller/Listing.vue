<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div>
  <div class="listing">
    <h1>Auction Listing</h1>
  </div>


  <v-container style="margin-top: 20px;">
    <v-row>
      <v-col cols="12" md="6" v-for="auction in auctions" :key="auction.id">
        <v-card>
          <v-img
            :src="auction.image"
            height="200"
          ></v-img>
          <v-card-title>{{ auction.name }}</v-card-title>
          <v-card-subtitle>{{ auction.description }}</v-card-subtitle>
          <v-card-text>
            <p>Current bid: {{ auction.currentBid }}</p>
            <p>Ends at: {{ auction.endsAt }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="placeBid(auction.id)">Place bid</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</div>
</template>

<script>
export default {
  data() {
    return {
    };
  },
  mounted() {
    // Fetch the auction data from the server and populate the auctions array
    this.fetchdata();
  },
  methods: {
    fetchdata() {
      // Replace this with the actual API call
    },

    placeBid(auctionId) {
      console.log(`Placing bid for auction with ID: ${auctionId}`);
    }
  }
};
</script>

<style scoped>
.listing {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 20px;
}

button {
  padding: 10px 20px;
}
</style>
