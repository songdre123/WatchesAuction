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
    this.publishablekey = "pk_test_51OrZSVC6Ev8NcoAAzjwUrkkQfpqoFasUwajb3GqNR7yGKt8EtSvS9Jjk4FFdaB4bUtvXVtQ0i9IsulHeU3HZUFEY00PTdyttJE"
    return {
        loading: false,
        lineItems: [
            {
            price: 'price_1OsMzwC6Ev8NcoAAflI50SEB',
            quantity: 1,
            }
        ],
        successUrl: 'http://localhost:8080/success',
        cancelUrl: 'http://localhost:8080/cancel',
        
    }
    },
    methods: {
        checkout(){
            this.$refs.CheckoutRef.redirectToCheckout()
        }
      
    }
    }
</script>