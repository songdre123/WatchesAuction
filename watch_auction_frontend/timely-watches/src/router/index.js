// Composables
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "Login",
    component: () => import("@/views/Login.vue"),
  },
  {
    path: "/checkout",
    name: "Checkout",
    component: () => import("@/views/Checkout.vue"),
  },
  {
    path: "/Success",
    name: "Success",
    component: () => import("@/views/Success.vue"), // Fixed the casing of the file name
  },
  {
    path: "/Cancel",
    name: "Cancel",
    component: () => import("@/views/Cancel.vue"),
  },
  {
    path: "/home",
    component: () => import("@/layouts/default/Default.vue"),
    children: [
      {
        path: "", // Empty path for the Home route
        name: "Home",
        component: () =>
          import(/* webpackChunkName: "home" */ "@/views/AuctionHome.vue"),
      },
      {
        path: "account", // Removed the leading slash
        name: "Account",
        component: () => import("@/views/Account.vue"),
      },
      {
        path: "/Create",
        name: "Create",
        component: () => import("@/views/Createlisting.vue"),
      }
    ],
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
