<template>
  <form @submit.prevent="handleSubmit">

    <div class="header-form">
      <h1>Login</h1>
    </div>

    <div class="name-fields">
      <label>First Name:</label>
      <input type="text" v-model="firstName" required />

    <div class="horizontal-space"></div>
      
      <label>Last Name:</label>
      <input type="text" v-model="lastName" required />
    </div>

    <label>Email:</label>
    <input type="email" v-model="email" required />

    <label>Password:</label>
    <input type="password" v-model="password" required />
    <div v-if="passwordError" class="error">{{ passwordError }}</div>

    <label>Phone Number:</label>
    <input type="text" v-model="phoneNumber" required pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}" placeholder="e.g., 94204837" />

    <label>Account Type:</label>
    <v-select v-model="accountType" :items="accountTypes">
    </v-select>

    <div class="terms">
      <input type="checkbox" v-model="terms" required />
      <label>Accept Terms and Conditions</label>
    </div>

    <div class="submit">
      <router-link to="/Home">
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
      accountType: "",
      accountTypes: ['Buyer', 'Seller'],
      terms: false,
      names: [],
      passwordError: ""
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
    }
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
  background: lightgoldenrodyellow;
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
