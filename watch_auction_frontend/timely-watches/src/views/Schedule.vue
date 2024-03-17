<template>
    <div class="container">
        <h1>Schedule Collection</h1>
        <p>Please select a date for collection of your watch.</p>
    </div>
    <form>
    <div class="wrapper">
        <ejs-calendar :selectedDate="date" :change="change" :showTodayButton="false">
        </ejs-calendar>
        <button @click.prevent="submitschedule" class="btn btn-primary">Submit</button>
    </div>
    </form>
    <div class="container">
    <div v-if="submitted">
        <h1>Success</h1>
        <p>Your collection date has been placed successfully.</p>
    </br>
        <p>your collection date is on {{date}}</p>
</br>
        <router-link to="/auctions" class="btn btn-primary">Back to Auctions</router-link>

    </div>
    <div v-if="tooearly">
        <h1>Too Early</h1>
        <p>You cannot schedule a collection before the next day or within 24 hours.</p>
    </div>
    </div>


</template>
<script>
import { CalendarComponent } from '@syncfusion/ej2-vue-calendars';
export default{
    name: 'Schedule',
    data(){
    return{
        date: new Date(),
        submitted: false,
        tooearly: false,
        id: ''
    }
},
components: {
    'ejs-calendar': CalendarComponent
},
methods: {
    change: function(args){
        this.date = args.value;
    },
    async submitschedule(){
        try{
            console.log(this.date);
            console.log(this.$route.params.id);
            this.id = this.$route.params.id;
            // await this.$http.put('//schedule/edit/${id}',{
            //     collection_date: this.date
            // });
            const today = new Date();
            today.setDate(today.getDate() + 1);
            if(this.date < today){
                this.tooearly = true;
            }
            else{
                this.submitted = true;
                this.tooearly = false;
            }

        }
        catch(error){
            console.log(error);
        }
    }
}
}

</script>

<style>
@import "@syncfusion/ej2-base/styles/material.css";
@import "@syncfusion/ej2-buttons/styles/material.css";
@import "@syncfusion/ej2-calendars/styles/material.css";
@import "bootstrap/dist/css/bootstrap.css"; /* Add this line */
.wrapper{
    max-width: 200px;
    margin: 0 auto;
}
.e-calendar {
    width: 500px; /* Adjust as needed */
}
.container{
    text-align: center;
}
</style>