<style>
.img-container {
  padding: 0 0px; /* Adjust as needed */
}
.my-table td, .my-table th {
  border: 1px solid #000; /* Add lines */
  padding: 10px; /* Add spacing */
}

</style>

<template>
    <v-container>
        <v-row align="center" justify="center">
            <v-col>
                <v-row>
                <v-form>
                    <h2 class="text">Pictures</h2>
                    <v-row>
                    <v-row>
                    <v-col cols="4" class="img-container" v-for="(file, index) in image_urls" :key="index">
                        <v-img
                            v-if="file"
                            :src="file"
                            width="250" 
                            height="250"
                        ></v-img>
                    </v-col>
                    </v-row>
                    </v-row>
                    <v-file-input
                    class="mt-4"
                    prepend-icon="mdi-camera"
                    placeholder="Select an image"
                    :chips="true"
                    :clearable="true"
                    :rounded="true"
                    @change="onFileChange"
                    width="200"
                    :show-size="true"
                    multiple
                    ></v-file-input>
                    <v-btn @click="uploadToS3">Upload Images</v-btn>
                    <!-- Show filename below -->
                </v-form>
            </v-row>

            <v-row>
                <v-col cols="12">
                    <h4>Suggested Prices</h4>
                </v-col>                
            </v-row>
            <v-row>
                <v-simple-table  class="my-table">
                    <template v-slot:default>
                        <thead>
                            <tr>
                                <th class="text-left">Average</th>
                                <th class="text-left">Mix</th>
                                <th class="text-left">Max</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{{avg_price}}</td>
                                <td>{{min_price}}</td>
                                <td>{{max_price}}</td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>
            </v-row>
            </v-col>


            <v-col cols="6" align="center" justify="center">
                <h2 class="text">Create a Listing</h2>
                <v-form>
                    <v-row class="mt-4">
                        <v-col cols="6">
                            <v-text-field label="Watch Name" required
                            v-model="Watch_name"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field label="Reference Number" required
                            v-model="reference_number"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-select
                            :items="['Rolex', 'Patek Philippe', 'Audemars Piguet']"
                            label="Brand"
                            v-model="brand"
                            required
                            >
                            </v-select>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field label="Year" required
                            v-model="year"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-checkbox
                            label="Watch Box"
                            v-model="Watch_box"
                            required
                            ></v-checkbox>
                        </v-col>
                        <v-col cols="6">
                            <v-checkbox
                            label="Watch Papers"
                            v-model="Watch_papers"
                            required
                            ></v-checkbox>
                        </v-col>
                        <v-col cols="12">
                            <v-select
                            :items="['New', 'Used']"
                            label="Watch Condition"
                            v-model="Watch_condition"
                            default-value="New"
                            required
                            ></v-select>
                        </v-col>
                        <v-col cols="12">
                            <!-- enter min bid amount -->
                            <v-text-field 
                            label="Minimum Bid" 
                            required
                            v-model="Minimum_bid"
                            :rules="[value => /^\d+$/.test(value) || 'Please enter an integer']"
                        ></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            Pick a starting date and time
                            <flat-pickr v-model="Start_date" :config="{enableTime: true, time_24hr: true}"></flat-pickr>
                          </v-col>
                        <v-col cols="6">
                            Pick an ending date and time
                            <flat-pickr v-model="End_date" :config="{enableTime: true, time_24hr: true}"></flat-pickr>  
                        </v-col>
                        <v-col cols="12">
                            <v-btn color="amber darken-2" @click="CreateListing">Create Listing</v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-col>
        </v-row>
    </v-container>
</template>







<script>

import AWS from 'aws-sdk';
import axios from 'axios';

import { ref } from 'vue';
import flatPickr from 'vue-flatpickr-component';
import 'flatpickr/dist/flatpickr.css';

export default {
components: {
    flatPickr,
},
setup(){
    const date = ref(null);
},
  data() {
    return {
        files: [],
        image_urls: [],
        Watch_name: null,
        reference_number: null,
        brand: null,
        year: null,
        Description: null,
        Minimum_bid: null,
        Start_date: null,
        End_date: null,
        Watch_box: false,
        Watch_papers: false,
        Watch_condition: "New",
        manufacturer_id: null,
        min_price: null,
        max_price: null,
        avg_price: null,
    };
  },
  watch: {
    reference_number: 'CheckSelection',
    brand: 'CheckSelection',
    year: 'CheckSelection',
  },
  methods: {
    onFileChange(e) {
        this.files = [];
        this.image_urls = [];
  const newFiles = Array.from(e.target.files);
  for (let i = 0; i < newFiles.length; i++) {
    if (this.files.length < 4) {
      this.files.push(newFiles[i]);
    } else {
      alert('You can only upload up to 3 images.');
      e.target.value = null; // Clear the file input
      this.files = []; // Clear the files array

      break;
    }
  }
},

    async GetSuggestedPrices() {
    // get suggested prices from the backend
    // use the watch name, reference number, brand, year, and condition
    // to get the suggested prices
    // then update the table
    if(this.brand=="Rolex"){
        this.manufacturer_id= "221";
    }
        else if(this.brand=="Patek Philippe"){
            this.manufacturer_id= "18";
        }
        else if(this.brand=="Audemars Piguet"){
            this.manufacturer_id= "223";
        }
    console.log(this.do);
    await axios.get('http://127.0.0.1:5000/scrape', {
        params: {
        "ref_number": this.reference_number,
        "manufacturer_id": this.manufacturer_id,
        "year": this.year,
        }
    })
        .then((response) => {
            console.log(response);
            console.log("response");
            this.items = response.data;
            this.avg_price = response.data.average_price;
            this.min_price = response.data.lowest_price;
            this.max_price = response.data.highest_price;
    }
        )
        .catch((error) => {
            console.log(error);
        });
    },
    CovertToTimestampfromStringStart(date) {
        let parts = date.split('/');
        let year = parts[0];
        let month = parts[1];
        let day = parts[2];
        let hour = parts[3];
        let minute = parts[4];

        this.Start_date = new Date(year, month - 1, day, hour, minute).getTime();
    },
    CovertToTimestampfromStringEnd(date) {
        let parts = date.split('/');
        let year = parts[0];
        let month = parts[1];
        let day = parts[2];
        let hour = parts[3];
        let minute = parts[4];

        this.End_date = new Date(year, month - 1, day, hour, minute).getTime();
    },
    CheckSelection() {
            console.log(this.reference_number);
            if (this.reference_number && this.brand && this.year) {
                this.GetSuggestedPrices();
        }
    }

    ,
    CreateListing() {
        // check if all fields are filled
        if (!this.Watch_name || !this.reference_number || !this.brand || !this.year || !this.Minimum_bid || !this.Start_date || !this.End_date ) {
            alert('Please fill in all fields.');
            return;
        }
        // check if the start date is before the end date
        if (this.Start_date >= this.End_date) {
            alert('The start date must be before the end date.');
            return;
        }
        // check if the minimum bid is a number
        if (isNaN(this.Minimum_bid)) {
            alert('The minimum bid must be a number.');
            return;
        }
        // check if the minimum bid is greater than 0
        if (this.Minimum_bid <= 0) {
            alert('The minimum bid must be greater than 0.');
            return;
        }
        // check if the watch condition is new or used
        if (this.Watch_condition !== 'New' && this.Watch_condition !== 'Used') {
            alert('The watch condition must be either "New" or "Used".');
            return;
        }
        // check if the number of images is less than 3
        if (this.image_urls.length < 3) {
            alert('You must upload at least 3 images.');
            return;
        }
        // upload to stripe
        else{
            console.log(this.Start_date);
            console.log(this.End_date);
            axios.post('http://127.0.0.1:5001/auction', {
                auction_item: this.Watch_name,
                watch_ref: parseInt(this.reference_number),
                watch_brand: this.brand,
                manufacture_year: this.year,
                auction_status: 0,
                auction_winner_id: null,
                start_price: parseInt(this.Minimum_bid),
                current_price: parseInt(this.Minimum_bid),
                start_time: this.Start_date,
                end_time: this.End_date,
                watch_box_present: this.Watch_box,
                watch_papers_present: this.Watch_papers,
                watch_condition: this.Watch_condition,
                watch_image1: this.image_urls[0],
                watch_image2: this.image_urls[1],
                watch_image3: this.image_urls[2],
            })
                .then((response) => {
                    console.log(response);
                    alert('Listing created successfully.');
                })
                .catch((error) => {
                    console.log(error);
                    alert('An error occurred. Please try again.');
                });
            }
        },
        async uploadToS3() { 
        // if number of files is more than 3, alert the user
        if (this.files.length > 3) {
            alert('You can only upload up to 3 images.');
            return;
        }
        if (!this.files) return;
    console
    this.files.forEach((file, index) => {
    let reader = new FileReader();

    reader.onload = (event) => {
        let fileContent = event.target.result;

        const accessKeyId = import.meta.env.VITE_APP_AWS_ACCESS_KEY_ID;
        const secretAccessKey = import.meta.env.VITE_APP_AWS_SECRET_ACCESS_KEY;
        console.log(accessKeyId);
        console.log(secretAccessKey);
        AWS.config.update({
            accessKeyId: accessKeyId,
            secretAccessKey: secretAccessKey,
            region: 'ap-southeast-1',
        });

        const s3 = new AWS.S3();
        const params = {
            Bucket: 'watchauctionimages',
            Key: `file-${index}-${file.name}`, // Unique key for each file
            Body: fileContent,
            ContentType: file.type,
        };

        s3.upload(params, (err, data) => {
    if (err) {
        console.log("Error", err);
    } if (data) {
        console.log("Upload Success", data.Location);
        this.image_urls.push(data.Location);
        this.files = [];
    }
});     
    };

    reader.readAsArrayBuffer(file);
});
    }


    }
    
    

  }
</script>
