// Composables
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "Login",
    component: () => import("@/views/Login.vue"),
  },
  {
    path: "/schedule/:id",
    name: "Schedule",
    component: () => import("@/views/Schedule.vue"),
  },
  {
    path:'/admin',
    component: () => import('@/layouts/admin/AdminDefault.vue'),
    children: [
      {
        path: "create",
        name: "Create",
        component: () => import("@/views/seller/CreateListing.vue")
      },
      {
        path: "account",
        name: "AdminAccount",
        component: () => import("@/views/Account.vue")
      },
      {
        path: "listing",
        name: "Listing",
        component: () => import("@/views/seller/Listing.vue")
      },
      {
        path:"auctionlist",
        name: "AuctionList",
        component: () => import("@/views/seller/ListOfAuctions.vue")
      }
    ]
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
        path:"bids",
        name: "Bids",
        component: () => import("@/views/BidsView.vue"),
      },
      {
        path: ":id",
        name: "AuctionDetails",
        component: () => import("@/views/AuctionDetails.vue"),
        meta: {
          auth: true,
        },
      },
      {
        path: "account", // Removed the leading slash
        name: "Account",
        component: () => import("@/views/Account.vue"),
      },
    ],
  },
  {
    path: "/checkout/:id",
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
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
