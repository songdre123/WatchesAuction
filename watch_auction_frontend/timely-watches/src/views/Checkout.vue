<!-- eslint-disable vue/multi-word-component-names -->
<template>
<div class="container">
  <div class="row">
    <div class="col-md-12">
      <h3>Details</h3>
      <div class="row">
        <div class="col-md-4">
          <img :src="watch_image1" alt="watch_image1" class="img-fluid" />
        </div>
        <div class="col-md-8">
          <h4>Name: {{ watchname }}</h4>
          <p>Brand: {{ brand }}</p>
          <p>Reference Number: {{ watchref }}</p>
          <p>Year: {{ manufacturer_year }}</p>
          <p>Price: {{ watchprice }}</p>
          <p>Auction Time: {{ auctiontime }}</p>
        </div>
    </div> 
    </div>
  <div class="row">
    <div class="col-md-12">
      <h1>Stripe Payment</h1>
      <h3>
        <button @click="redirectToCheckout">Click to make deposit</button>
      </h3>
    </div>
  </div>
</div>
</div>
</template>

<script>
import axios from 'axios';
import { useUserStore } from '@/store/userStore';
const userStore = useUserStore();
const userid = userStore.userID;

export default {
  data() {
    return {
      checkoutUrl: null,
      watchname: null,
      manufacturer_year: null,
      brand: null,
      watch_image1: null,
      watchref: null,
      watchprice: null,
      auctiontime: null,
      winner: '',

    };
  },
  methods: {
        async beforeenter(to, from, next){
        const response = await axios.get(`http://127.0.0.1:5001/auction/${this.$route.params.id}`)
        this.winner = response.data.data.auction_winner_id;
        if(this.winner !== userid){
            next('/home');
        }
        else  
            next();
        },
    redirectToCheckout() {
      if (this.checkoutUrl) {
        window.location.href = this.checkoutUrl;
      }
    },
  },
  beforeRouteEnter(to, from, next) {
    axios.get(`http://127.0.0.1:5001/auction/${to.params.id}`)
      .then(response => {
        next(vm => {
          vm.checkoutUrl = response.data.data.stripe_product_id;
          vm.watchname = response.data.data.auction_item;
          vm.manufacturer_year = response.data.data.manufacture_year;
          vm.brand = response.data.data.watch_brand;
          vm.watch_image1 = response.data.data.watch_image1;
          vm.watchref = response.data.data.watch_ref;
          vm.watchprice = response.data.data.current_price;
          vm.auctiontime = response.data.data.end_time;
        });
      })
      .catch(error => {
        console.log(error);
        next(false);
      });
  },
  created() {
    this.beforeenter();
  },
};
</script>