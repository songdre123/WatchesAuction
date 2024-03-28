// Utilities
import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null,
    userID: null,
    isLoggedIn: false,
  }),
  actions: {
    async setUser(user) {
      this.user = user;
      return new Promise((resolve) => {
        // Simulate asynchronous operation to set user data
        setTimeout(() => {
          resolve(); // Resolve the promise once user data is set
        }, 100); // Adjust the delay as needed
      });
    },
    async loginAuth(user_email, params) {
      try {
        const response = await axios.post(
          `http://127.0.0.1:5000/user/login/${user_email}`,
          params
        );
        if (response.data.code == 200) {
          try {
            const userResponse = await axios.get(
              `http://127.0.0.1:5000/user/${user_email}`
            );
            const userData = userResponse.data.data;
            if (!userData) {
              console.error("User data not found");
              return;
            }
            const userID = userData.id;
            this.setUser(userData);
            this.setUserId(userID);
            this.isLoggedIn = true;
          } catch (error) {
            console.error("There was a problem with the request", error);
            console.log(error.message);
            console.log(error.data);
          }
        }
      } catch (error) {
        console.error("There was a problem with the request", error);
        console.log(error.message);
        console.log(error.data);
      }
    },
    setUserId(id) {
      this.userID = id;
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve();
        }, 100);
      });
    },
    getUser() {
      return this.user;
    },
    getUserId() {
      return this.userID;
    },
    getUserName() {
      return this.user.first_name + " " + this.user.last_name;
    },
    getUserEmail() {
      return this.user.email;
    },
    removeUser() {
      this.user = "";
    },
    editImage(photo_link) {
      this.user.profile_picture = photo_link;
    },
    editFirstName(firstName) {
      this.user.first_name = firstName;
    },
    editLastName(lastName) {
      this.user.last_name = lastName;
    },
    editPassword(password) {
      this.user.password = password;
    },
    logout() {
      this.isLoggedIn = false;
    },
  },
  persist: {
    enabled: true,
  },
});
