<template>
    <v-container>
        <v-row align="center" justify="center">
            <v-col>
                <v-row>
                <v-form>
                    <h2 class="text">Pictures</h2>
                    <div v-for="(file, index) in image_urls" :key="index">
                        <v-img
                            v-if="image_urls[index]"
                            :src="image_urls[index]"
                            width="200"
                            height="200"
                            contain
                        ></v-img>
                    </div>
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
                            v-model="Reference_number"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field label="Brand" required
                            v-model="Brand"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field label="Year" required
                            v-model="Year"
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
                        <v-col cols="6">
                            <v-text-field label="Minimum Bid" required></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field label="Start date and time" required></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field label="End date and time" required></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-btn color="amber">Create</v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-col>
        </v-row>
    </v-container>
</template>







<script>

import AWS from 'aws-sdk';

export default {
  data() {
    return {
        files: [],
        image_urls: [],
        Watch_name: null,
        Reference_number: null,
        Brand: null,
        Year: null,
        Description: null,
        Minimum_bid: null,
        Start_date: null,
        End_date: null,
        Watch_box: null,
        Watch_papers: null,
        Watch_condition: "New"
    
    };
  },
  methods: {
    onFileChange(e) {
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
CovertToTimestampfromString(date) {
    return new Date(date).getTime() / 1000;
}
,
    uploadToS3() {
        // if number of files is more than 3, alert the user
        if (this.files.length > 3) {
            alert('You can only upload up to 3 images.');
            return;
        }
        if (!this.files) return;

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
