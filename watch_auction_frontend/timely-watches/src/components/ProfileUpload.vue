<template>
  <v-container>
    <v-row align="center" justify="center">
      <!-- Align cols to the center -->
      <v-col cols="4" align="center">
        <v-form>
          <h2 class="text">Profile Picture</h2>
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
          <!-- Show filename below -->
          <v-row v-if="file">
            <v-col>
              <p>File: {{ file.name }}</p>
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

          const accessKeyId = import.meta.env.VITE_ENV_AWS_ACCESS_KEY_ID;
          const secretAccessKey = import.meta.env.VITE_ENV_AWS_SECRET_ACCESS_KEY;

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

@font-face {
  font-family: Riviera Nights;
  src: url(@/styles/rivieraNights/RivieraNights-Regular.otf)
}

.text {
  font-family: Riviera Nights, sans-serif;
  font-style: italic;
}


</style>
