<template>
    <div class="card">

      <div class="card-header text-center">
        <h5>{{ date }}</h5>
      </div>
  
      <div class="card-body" :style="{ backgroundImage: 'url(' + imageUrl + ')' }">
 
        <div class="card-title text-center text-white">
          <h4>{{ watchName }}</h4>
          <p>Reference Number: {{ referenceNumber }}</p>
          <p>Opening Bid: {{ openingBid }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        imageUrl: '',
        date: '',
        watchNam: '',
        referenceNumber: '',
        openingBid: 0,
      };
    },
    created() {
      this.fetchImage();
      this.fetchListingDetails();
    },
    methods: {
      fetchImage() {
        //
      },
      fetchListingDetails() {
        //
      },

    },
  };
  </script>
  
  <style scoped>
  .card {
    margin: 20px;
  }
  
  .card-body {
    height: 200px;
    background-size: cover;
    background-position: center;
  }
  
  .card-title {
    position: absolute;
    bottom: 0;
    width: 100%;
    padding: 15px;
    background-color: rgba(0, 0, 0, 0.7);
  }
  </style>
  