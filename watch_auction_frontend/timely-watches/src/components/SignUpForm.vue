<template>
  <form @submit.prevent="handleSubmit">

    <div class="header-form">
      <h1>Login</h1>
    </div>

    <div class="name-fields">
      <label>First Name:</label>
      <input type="text" v-model="firstName" />

    <div class="horizontal-space"></div>
      
      <label>Last Name:</label>
      <input type="text" v-model="lastName" />
    </div>

    <label>Email:</label>
    <input type="email" v-model="email" required />

    <span>
    <label>Password:</label>
     <v-btn size="xs" class="password-toggle" @click="togglePasswordVisibility">
      {{ showPassword ? 'Hide' : 'Show' }} Password
    </v-btn>
    </span>
    <input :type="showPassword ? 'text' : 'password'" v-model="password" required />
    <div v-if="passwordError" class="error">{{ passwordError }}</div>

    <label>Phone Number:</label>
    <input type="text" v-model="phoneNumber" required pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}" placeholder="e.g., 94204837" />

    <label>Account Type:</label>
    <v-select v-model="accountType" :items="accountTypes" required>
    </v-select>

    <label>Profile Picture:</label>
    <v-file-input
    :rules="rules"
    accept="image/png, image/jpeg, image/bmp, image/jpg"
    label="Profile Photo"
    placeholder="Choose profile photo"
    prepend-icon="mdi-camera"
    loading="true"
    ></v-file-input>

    <div class="terms">
      <input type="checkbox" v-model="terms" required />
      <label>Accept Terms and Conditions</label>
    </div>

    <div class="submit">
      <router-link to="/home">
        <v-btn size="small" class="pill" @click="handleSubmit">Create an account</v-btn>
      </router-link>
    </div>
  </form>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
      showPassword: false,
      accountType: "",
      accountTypes: ['Buyer', 'Seller'],
      terms: false,
      names: [],
      passwordError: "",
      fileRules: [
      value => {
        const acceptedFormats = ['image/png', 'image/jpeg', 'image/bmp', 'image/jpg'];
        const allowedSize = 2000000; // 2MB in bytes
        const file = value && value.length ? value[0] : null;
        if (!file) return 'Please select a file.';
        if (!acceptedFormats.includes(file.type)) return 'Only image formats (PNG, JPEG, BMP, JPG) are allowed.';
        if (file.size > allowedSize) return 'Profile picture size should be less than 2 MB!';
        return true;
      },
    ],
    }
  },
  methods: {
    handleSubmit() {
      // validate password
      this.passwordError = this.password.length > 5 ? 
        "" : "Password must at least be 6 characters long"

      if (!this.passwordError) {
        console.log('Logged In')
      }
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
  }

}
</script>

<style scoped>

@font-face {
  font-family: Riviera Nights Light;
  src: url(@/styles/rivieraNights/RivieraNights-Light.otf);
}

@font-face {
  font-family: Riviera Nights Bold;
  src: url(@/styles/rivieraNights/RivieraNights-Bold.otf)
}
form {
  min-width: 500px;
  margin: 30px auto;
  background: white;
  text-align: left;
  padding: 20px;
  border-radius: 10px;
  font-family: Riviera Nights Light;
}

label {
  color: darkgray;
  display: inline-block;
  margin: 10px 0 10px;
  font-size: 0.6em;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: bold;
}

input, select {
  display: block;
  padding: 10px 6px;
  width: 100%;
  box-sizing: border-box;
  border: none;
  border-bottom: 1px solid #ddd;
  color: #555;
}

input[type="checkbox"] {
  display:inline-block;
  width: 16px;
  margin: 0 10 0 0;
  position: relative;
  top: 2px;
}

.header-form {
  font-family: Riviera Nights Bold, sans-serif;
  margin-bottom: 10px;
}

.password-toggle {
  font-size: 12px;
  margin-left: 350px;
}

.pill {
  display: inline-block;
  margin: 20px 10px 0 0;
  padding: 6px 12px;
  background: #eee;
  border-radius: 20px;
  font-size: 12px;
  letter-spacing: 1px;
  font-weight: bold;
  color: #777;
  cursor: pointer;
}

.submit{
  text-align: center;
}

.error {
  color: #ff0062;
  margin-top: 10px;
  font-size: 0.8em;
  font-weight: bold;
}

.name-fields {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.horizontal-space {
  width: 10px; /* Adjust the width according to your preference */
}




</style>
