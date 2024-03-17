<!-- eslint-disable vue/multi-word-component-names -->
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
        prod_id: '',
        lineItems: [
            {
            price: '',
            quantity: 1,
            }
        ],
        successUrl: 'http://localhost:3000/success?session_id={id}',
        cancelUrl: 'http://localhost:3000/cancel',
        
    }
    },
    async created(){
        const id= this.$route.params.id;
        try{
            const response = await this.$http.get(`/auction/${id}`);
            this.prod_id = response.data.stripe_product_id;
            const prod_details = await stripe.products.retrieve(this.prod_id);
            this.lineItems[0].price = prod_details.prices.data[0].id;
        }catch(error){
            console.log(error);
        }
    }
    ,
    methods: {
        checkout(){
            this.$refs.CheckoutRef.redirectToCheckout()
        
    }
}
</script>