import axios from "axios";
// eslint-disable-next-line no-unused-vars
const baseURL = "http://localhost:3000";
const axiosIns = axios.create;
({
  headers: {
    Accepts: "application/json",
    "Access-Control-Allow-Origin": "*",
  },
  baseURL: "/api",
});

export default axiosIns;
