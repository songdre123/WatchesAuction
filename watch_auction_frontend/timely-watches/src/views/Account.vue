<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <!-- Include profile picture and allow user to upload image -->
    <div>
    <v-container>
    <v-row align="center" justify="center">
      <!-- allign cols to the center -->
      <v-col cols="6" align="center">

        <h2>Profile Picture</h2>
        
        <v-img
        v-if="image_url"
        :src="image_url"
        class="profile-picture rounded-circle mt-4"
        width="200"
        height="200"
        contain
        ></v-img>
        <v-img
        v-else
        src="https://via.placeholder.com/200"
        class="profile-picture rounded-circle mt-4"
        width="200"
        height="200"
        contain
        ></v-img>

    
        <v-file-input
        class="mt-4"
        v-model="file"
        label="Select an image"
        :chips="true"
        :clearable="true"
        :rounded="true"
        @change="onFileChange"
        width="200"
        :show-size="true"
        ></v-file-input>
        <v-btn @click="uploadToS3">Upload</v-btn>
        <!-- show filename below -->
        <v-row v-if="file">
        <v-col>
            <p>File: {{ file.name }}</p>
        </v-col>
        </v-row>

        
      </v-col>
    </v-row>
    </v-container>
    
    <v-container>
      <v-row align="center" justify="center">
          <v-col cols="6" align="center" justify="center">
            <h2>Account Settings</h2>
                <v-form>
                    <v-row>
                        <v-col cols="6">
                            <v-text-field label="First Name" required></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field label="Last Name" required></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field label="Email" required></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field label="Password" required></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-btn color="amber">Save</v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-col>
        </v-row>
    </v-container>

    </div>


</template>




<script>
import AWS from 'aws-sdk';

export default {
    data() {
  return {
    file: null,
    image_url: null,
  };
},
methods: {
  onFileChange(e) {
    this.file = e.target.files[0];
  },

  uploadToS3() {
  if (!this.file) return;

  let files = Array.isArray(this.file) ? this.file : [this.file]; // Ensure files is always an array

  files.forEach(file => {
    let reader = new FileReader();

    reader.onload = (event) => {
      let fileContent = event.target.result;

    const accessKeyId = import.meta.env.ENV_AWS_ACCESS_KEY_ID;
    const secretAccessKey = import.meta.env.ENV_AWS_SECRET_ACCESS_KEY;

    AWS.config.update({
        accessKeyId: accessKeyId,
        secretAccessKey: secretAccessKey,
        region: 'ap-southeast-1',
      });

    const s3 = new AWS.S3();
    const params = {
      Bucket: 'watchauctionimages',
      Key: "profile-pic-test.jpg",
      Body: fileContent,
      ContentType: this.file.type,
      ACL: 'public-read',
    };

            s3.upload(params, (err, data) => {
        if (err) {
            console.log('Error uploading image:', err);
        } else {
            console.log('Image uploaded successfully to S3. URL:', data.Location);
            this.image_url = data.Location + '?' + new Date().getTime();
        }
        });
    };

    reader.readAsArrayBuffer(file);
  });
}
}
}


</script>

<style scoped>



</style>