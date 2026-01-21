<template>
  <div class="main_auth_page">
    <div class="auth_card">
      <h1>Вход в систему</h1>
      <div class="form_item">
        <label>Email:</label>
        <input type="text" v-model="email" placeholder="Введите email" />
      </div>
      <div class="form_item">
        <label>Пароль:</label>
        <input
          type="password"
          v-model="password"
          placeholder="Введите пароль"
        />
      </div>
      <p class="error_text" v-if="error">{{ error }}</p>
      <div class="buttons_row">
        <button @click="Post_Login">Войти</button>
        <button class="secondary_btn" @click="$emit('emit_to_register')">
          Нет аккаунта?
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { Axios_Post } from "../index.js";

export default {
  data() {
    return { email: "", password: "", error: "" };
  },
  methods: {
    async Post_Login() {
      if (this.email == "" || this.password == "") {
        this.error = "Заполните все поля";
        return;
      }
      try {
        const response = await Axios_Post("/login", {
          email: this.email,
          password: this.password,
        });
        this.$emit(
          "emit_login_success",
          response.data.first_name,
          response.data.user_id,
        );
        this.email = "";
        this.password = "";
        this.error = "";
      } catch (e) {
        this.error =
          e.response?.data?.message || "Ошибка соединения с сервером";
      }
    },
  },
};
</script>

<style scoped>
.main_auth_page {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 100px;
}
.auth_card {
  background-color: aliceblue;
  width: 400px;
  border: 2px solid steelblue;
  border-radius: 15px;
  padding: 30px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.form_item {
  display: flex;
  flex-direction: column;
}
.form_item input {
  font-size: 18px;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
}
.error_text {
  color: red;
  text-align: center;
}
.buttons_row {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}
button {
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
}
.secondary_btn {
  background-color: #ddd;
  color: black;
}
</style>
