<template>
  <div class="admin-app">
    <Login v-if="!isLogged" @emit_login_success="handleLoginSuccess" />

    <Dashboard v-else @logout="handleLogout" />
  </div>
</template>

<script>
import Login from "./components/Login.vue";
import Dashboard from "./components/Dashboard.vue";
import { Axios_Get } from "./index.js";

export default {
  components: {
    Login,
    Dashboard,
  },
  data() {
    return {
      isLogged: false,
    };
  },
  methods: {
    async checkAuth() {
      try {
        await Axios_Get("/admin/users");
        this.isLogged = true;
      } catch (e) {
        this.isLogged = false;
      }
    },
    handleLoginSuccess() {
      this.isLogged = true;
    },
    handleLogout() {
      this.isLogged = false;
    },
  },
  mounted() {
    this.checkAuth();
  },
};
</script>

<style>
body {
  margin: 0;
  font-family: sans-serif;
  background-color: #f4f4f9;
}
.admin-app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>
