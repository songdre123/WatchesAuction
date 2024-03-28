<template>
    <form @submit.prevent="login">

    <div class="header-form">
      <h1>Login</h1>
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

    <div class="submit">
        <v-btn type="submit" size="small" class="pill">Log In</v-btn>
    </div>
  </form>
</template>

<script>
import { useUserStore } from '@/store/userStore'


export default {
  data() {
    return {
      email: "",
      password: "",
      showPassword: false,
      passwordError: "",
    }
  },
  methods: {
     async login() {
      const data = {
        password: this.password,
      };

      const userStore = useUserStore()

      try {
        await userStore.loginAuth(this.email, data);

        // Now, check the isLoggedIn status after the login process is completed
        console.log(userStore.isLoggedIn);

        if (userStore.isLoggedIn) {
          console.log(userStore.user.account_type);
          if (userStore.user.account_type === 'Buyer') {
            this.$router.push({ path: '/home' });
          } else {
            this.$router.push({ path: '/admin' });
          }
        }
      } catch (error) {
        console.error(error, error.message);
      }
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

<!-- // axios.post(`http://127.0.0.1:5000/user/login/${this.email}`, data)
      //   .then(response => {
      //     console.log(response.data);
      //   })
      //   .catch(error => {
      //     // Handle errors
      //     console.error("There was a problem with the request:", error);
      //   });

      //   try {
      //     const userResponse = await axios.get(`http://127.0.0.1:5000/user/${this.email}`)
      //     const userData = userResponse.data.data
      //     const userID = userData.id
      //     userStore.setUserId(userID)
      //     userStore.setUser(userData)

      //       if (userData.account_type == 'Buyer') {
      //         this.$router.push({path: '/home'})
      //       }
      //       else {
      //         this.$router.push({path: '/admin'})
      //       }
          
      //     console.log(userID)

      //   } catch (error) {
      //   console.error('Error getting user:', error.message);
      //   throw error; // Re-throw the error to propagate it further
      //   }
       -->