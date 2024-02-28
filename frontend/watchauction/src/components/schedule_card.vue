<template>
    <div class="container mt-5">
      <div class="row">
        <div class="col-md-6 mx-auto">
          <h2 class="text-center mb-4">Schedule TESTING</h2>
  
          <div v-for="schedule in schedules" :key="schedule.auction_id" class="card mb-3">
            <div class="card-header">
              <h5 class="card-title">{{ formatDate(schedule.collection_time) }}</h5>
            </div>
            <div class="card-body">
              <h4 class="card-title">{{ schedule.auction_id }}</h4>
              <p class="card-text">Customer: {{ schedule.user_id }}</p>
            </div>
          </div>
  
          <!-- Create Schedule Form -->
          <form @submit.prevent="createSchedule">
            <div class="mb-3">
              <label for="newAuctionId" class="form-label">Auction ID</label>
              <input type="number" class="form-control" id="newAuctionId" v-model="newSchedule.auction_id" required>
            </div>
            <button type="submit" class="btn btn-success">Create Schedule</button>
          </form>
  
            <!-- Edit Schedule Form -->
            <form @submit.prevent="editSchedule">
                <div class="mb-3">
                    <label for="editAuctionId" class="form-label">Auction ID</label>
                    <input type="number" class="form-control" id="editAuctionId" v-model="editedSchedule.auction_id" required>
                </div>
                <div class="mb-3">
                    <label for="editUserId" class="form-label">User ID</label>
                    <input type="number" class="form-control" id="editUserId" v-model="editedSchedule.user_id" required>
                </div>
                <div class="mb-3">
                    <label for="editCollectionTime" class="form-label">Collection Time</label>
                    <input type="datetime-local" class="form-control" id="editCollectionTime" v-model="editedSchedule.collection_time" required>
                </div>
                <button type="submit" class="btn btn-warning">Edit Schedule</button>
            </form>
  
          <!-- Delete Schedule Form -->
          <form @submit.prevent="deleteSchedule">
            <button type="submit" class="btn btn-danger">Delete Schedule</button>
          </form>
  
          <!-- Fetch Schedules Button -->
          <button @click="fetchSchedules" class="btn btn-primary mt-3">Fetch Schedules</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        schedules: [],
        newSchedule: {
          auction_id: null,
        },
        editedSchedule: {
        auction_id: null,
        user_id: null,
        collection_time: null,
      },
      };
    },
    methods: {
      fetchSchedules() {
        // Fetch schedules from API
        // Example using fetch API
        fetch('http://localhost:5001/schedule')
          .then(response => response.json())
          .then(data => {
            this.schedules = data;
          })
          .catch(error => {
            console.error('Error fetching schedules:', error);
          });
      },
      createSchedule() {
      // Create a new schedule
      // Example using fetch API with POST method
      fetch('http://localhost:5001/schedule/create/' + this.newSchedule.auction_id, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.newSchedule),
      })
        .then(response => response.json())
        .then(data => {
          console.log('Schedule created:', data);
          this.fetchSchedules(); // Refresh the schedule list after creating
          this.newSchedule.auction_id = null; // Reset input field
        })
        .catch(error => {
          console.error('Error creating schedule:', error);
        });
    },

    editSchedule() {
      // Edit an existing schedule
      // Example using fetch API with PUT method
      fetch('http://localhost:5001/schedule/edit/' + this.editedSchedule.auction_id, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: this.editedSchedule.user_id,
          collection_time: this.editedSchedule.collection_time,
        }),
      })
        .then(response => response.json())
        .then(data => {
          console.log('Schedule edited:', data);
          this.fetchSchedules(); // Refresh the schedule list after editing
          this.editedSchedule.auction_id = null; // Reset input fields
          this.editedSchedule.user_id = null;
          this.editedSchedule.collection_time = null;
        })
        .catch(error => {
          console.error('Error editing schedule:', error);
        });
    },

    deleteSchedule() {
      // Delete a schedule
      // Example using fetch API with DELETE method
      fetch('http://localhost:5001/schedule/delete/' + this.editedSchedule.auction_id, {
        method: 'DELETE',
      })
        .then(response => response.json())
        .then(data => {
          console.log('Schedule deleted:', data);
          this.fetchSchedules(); // Refresh the schedule list after deleting
          this.editedSchedule.user_id = null; // Reset input field
        })
        .catch(error => {
          console.error('Error deleting schedule:', error);
        });
    },
      formatDate(date) {
            return date
      },
      formatCurrency(amount) {
            return '$' + amount.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your custom styles here */
  </style>
  