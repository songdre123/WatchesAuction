<template>
  <div class="listing">
    <h1>Auction Listing</h1>
    
  </div>
</template>

<script>
export default {
  data() {
    return {
      auctions: [] // Array to store the auction data
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
