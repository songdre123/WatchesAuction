<!-- eslint-disable vue/multi-word-component-names -->
<template>
<h1>Stripe Payment</h1>


<button @click="redirectToCheckout">Click to make deposit</button>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      checkoutUrl: null,
      stripe: null,
      key: null,
    };
  },
  methods: {
    redirectToCheckout() {
      if (this.checkoutUrl) {
        window.location.href = this.checkoutUrl;
      }
    },
    async getCheckoutUrl() {
      try {
    const response = await axios.get(`http://127.0.0.1:5001/auction/${this.$route.params.id}`);
    console.log(`http://127.0.0.1:5001/auction/${this.$route.params.id}`);
       this.checkoutUrl = response.data.data.stripe_product_id;
      } catch (error) {
        console.log(error);
      }
    },
  },
    mounted() {
    this.key = import.meta.env.VUE_APP_STRIPE_PUBLISHABLE_KEY;  // Add this line
    console.log(this.key);
    this.stripe = window.Stripe(this.key);
    },
  created() {
    this.getCheckoutUrl();
  },
};
</script>