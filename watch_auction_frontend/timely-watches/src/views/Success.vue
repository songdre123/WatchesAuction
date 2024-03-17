<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div>
        <h1>Success</h1>
        <p>Your Deposit has been placed successfully.</p>
    </div>
</template>
<script>
export default {
    name: 'Success',
    data() {
        return {
            loading: false,
        }
    },
    methods: {
        async changestatus(){
            await axios.put(`/auction/${this.$route.params.id}`,{
                auction_status: -2
            })
        }
    },
    async mounted(){
        await this.changestatus();
    }
}


</script>