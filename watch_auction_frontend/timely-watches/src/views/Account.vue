<style scoped>
.profile-picture {
  border-radius: 50%;
}
</style>


<template>
    <!-- Include profile picture and allow user to upload image -->

    <v-container>
    <v-row align="center" justify="center">
      <!-- allign cols to the center -->
      <v-col cols="12" align="center">

        <h1>Profile Picture</h1>
        
        <v-img
        v-if="image_url"
        :src="image_url"
        class="profile-picture"
        width="200"
        height="200"
        contain
        ></v-img>
        <v-img
        v-else
        src="https://via.placeholder.com/200"
        class="profile-picture"
        width="200"
        height="200"
        contain
        ></v-img>

    
        <v-file-input
        v-model="file"
        label="Select an image"
        @change="onFileChange"
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
            <v-col cols="12" align="center">
                <h1>Account Settings</h1>
            </v-col>
            <v-col cols="12">
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
                            <v-btn color="primary">Save</v-btn>
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

    AWS.config.update({
        accessKeyId: 'AKIATIQ6R7O5UWEDQAUM',
        secretAccessKey: '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',
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