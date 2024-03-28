 <template>
    <div class="container">
        <h1>Schedule Collection</h1>
        <p>Please select a date for collection of your watch.</p>
    </br>
        <p>Collection is available from 9am to 5pm. Please note that
            collection date once selected can only be changed by contacting us.</p>
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
        <p>Thank you for choosing Timely Watches.</p>
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
import axios from 'axios';
import { CalendarComponent } from '@syncfusion/ej2-vue-calendars';
import { useUserStore } from '@/store/userStore';
const userStore = useUserStore();
const userid = userStore.userID;
export default{
    name: 'Schedule',
    data(){
    return{
        date: new Date(),
        submitted: false,
        tooearly: false,
        id: '',
        winner: '',
       
    }

    
},
components: {
    'ejs-calendar': CalendarComponent
},
methods: {
    change: function(args){
        this.date = args.value;
    },
    async beforeenter(next){
        await axios.get(`http://127.0.0.1:5001/auction/${this.$route.params.id}`)
        this.winner = response.data.data.auction_winner_id;
        if(this.winner !== userid){
            console.log("You can be here!")
            next('/home');
        }
        else
            console.log("You can be here!")
            next();
        },
    async submitschedule(){
        try{
            // Convert this.date to a string in the "yyyy-mm-dd" format
            const formattedDate = this.date.toISOString().slice(0, 10);
            console.log(formattedDate);
            console.log(this.$route.params.id);
            this.id = this.$route.params.id;

            const today = new Date();
            today.setDate(today.getDate() + 1);
            console.log(this.id);
            if(this.date < today){
                this.tooearly = true;
            }
            else{
                const response = await axios.put(`http://127.0.0.1:5003/schedule/edit/${this.id}`, {
                    collection_date: formattedDate,
                    user_id: userid
                    // for ethan to settle session variable <3
                });

                if(response.status === 200){
                    this.submitted = true;
                    this.tooearly = false;
                }
            }
        }
        catch(error){
            console.log(error);
        }
    },
    async update_status(){
        try{
            console.log(this.$route.params.id);

            const response = await axios.put(`http://127.0.0.1:5001/auction/${this.$route.params.id}`, {
                auction_status: -2
            });
            console.log(response);
        }
        catch(error){
            console.log(error);
        }
    }
},

created(){
    this.beforeenter();
    this.update_status();
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