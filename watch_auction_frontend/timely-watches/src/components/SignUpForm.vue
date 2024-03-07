<template>
  <form @submit.prevent="handleSubmit">
    <label>Email:</label>
    <input type="email" v-model="email" required />

    <label>Password:</label>
    <input type="password" v-model="password" required />
    <div v-if="passwordError" class="error">{{ passwordError }}</div>

    <label>Account Type:</label>
    <v-select v-model="accountType" :items="accountTypes">
    </v-select>

    <label>Skills:</label>
    <input type="text" v-model="tempSkill" @keyup.enter="addSkill"/>
    <div v-for="skill in skills" :key="skill" class="pill" @click="removeSkill(skill)">
      {{ skill }}
    </div>

    <div class="terms">
      <input type="checkbox" v-model="terms" required />
      <label>Accept Terms and Conditions</label>
    </div>

    <div class="submit">
      <router-link to="/Home">
        <v-btn size="small" color="primary" @click="handleSubmit">Create an account</v-btn>
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
      tempSkill: '',
      skills: [],
      passwordError: ""
    }
  },
  methods: {
    addSkill(e) {
      if (e.key === 'Enter') {
        const newSkill = this.tempSkill.trim()
        if (newSkill && !this.skills.includes(newSkill)) {
          this.skills.push(newSkill);
        }
        this.tempSkill = ""
      }
    },
    removeSkill(skill) {
      this.skills = this.skills.filter((s) => {return skill !== s})
    },
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

form {
  min-width: 500px;
  margin: 30px auto;
  background: lightgoldenrodyellow;
  text-align: left;
  padding: 20px;
  border-radius: 10px;
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


</style>
