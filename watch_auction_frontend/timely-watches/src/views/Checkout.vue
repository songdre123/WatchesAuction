<template>
<h1>Stripe Payment</h1>
<stripe-checkout
ref= "CheckoutRef"
mode="payment"
:pk='publishablekey'
:line-items="lineItems"
:success-url="successUrl"
:cancel-url="cancelUrl"
@loading="v=>loading = v"
/>
<button @click="checkout">Pay Now</button>
</template>

<script>
import {StripeCheckout} from 'vue-stripe-checkout'
export default {
  components: {
    StripeCheckout
  },
  data() {
    this.publishablekey = "pk_live_51OrZSVC6Ev8NcoAARa1n6fdYKRWNZMJJ0n9L9aIsArHZncbtPdKc0K2qYv306dERk0iA8lx7TIA6pTWxHMN0UMSB00sptNLtJ4"
    return {
        loading: false,
        publishablekey: null,
        lineItems: [
            {
            name: 'Watch Deposit',
            quantity: 1,
            amount: 1
            }
        ],
        successUrl: 'http://localhost:8080/success',
        cancelUrl: 'http://localhost:8080/cancel',
        
    }
    },
    methods: {
      
    }
    }
</script>