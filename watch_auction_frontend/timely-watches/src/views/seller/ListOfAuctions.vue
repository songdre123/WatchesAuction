<template>
    <v-card flat>
      <v-card-title class="d-flex align-center pe-2">
        <v-icon icon="mdi-video-input-component"></v-icon> &nbsp;
        Find an auction
  
        <v-spacer></v-spacer>
  
        <v-text-field
          v-model="search"
          density="compact"
          label="Search"
          prepend-inner-icon="mdi-magnify"
          variant="solo-filled"
          flat
          hide-details
          single-line
        ></v-text-field>
      </v-card-title>
  
      <v-divider></v-divider>

      <v-data-table v-model:search="search" :items="items" :headers="headers" item-key="auction_id">
        <template v-slot:item.auction_id="{ item }">
    {{ item.auction_id }}
        </template>

  <template v-slot:item.auction_item="{ item }">
    {{ item.auction_item }}
  </template>
  
<template v-slot:item.start_time="{ item }">
    {{ item.start_time }}
    </template> 
    <template v-slot:item.end_time="{ item }">
    {{ item.end_time }}
    </template>

  <template v-slot:item.watch_image1="{ item }">
    <v-img v-if="item.watch_image1" :src="item.watch_image1" height="64" cover></v-img>
  </template>

  <template v-slot:item.watch_image2="{ item }" >
    <v-img v-if="item.watch_image2" :src="item.watch_image2" height="64" cover></v-img>
  </template>

  <template v-slot:item.watch_image3="{ item }">
    <v-img v-if="item.watch_image3" :src="item.watch_image3" height="64" cover></v-img>
  </template>
        </v-data-table>
        </v-card>
  </template>
  
  <script>
    import axios from 'axios';

    export default {
  name: 'ListOfAuctions',
  data() {
    return {
      search: '',
      items: [],
      headers: [
        { text: 'Auction ID', value: 'auction_id' },
        { text: 'Auction Item', value: 'auction_item' },
        { text: 'Start Time', value: 'start_time' },
        { text: 'End Time', value: 'end_time' },
        { text: 'Image 1', value: 'watch_image1' },
        { text: 'Image 2', value: 'watch_image2' },
        { text: 'Image 3', value: 'watch_image3' },
        ],
    };
  },
  methods: {
    async getAuctions() {
      const response = await axios.get('http://127.0.0.1:5001/auction');
      console.log(response.data.data.auctions);
      this.items = response.data.data.auctions;
      
    },
  },
  created() {
    this.getAuctions();
  },
};
  </script>