<template>
  <div class="main_auth_page">
    <div class="auth_card">
      <h1>Регистрация</h1>
      <div class="form_item">
        <label>Имя:</label>
        <input type="text" v-model="first_name" placeholder="Ваше имя" />
      </div>
      <div class="form_item">
        <label>Фамилия:</label>
        <input
          type="text"
          v-model="last_name"
          placeholder="Ваша фамилия (необязательно)"
        />
      </div>
      <div class="form_item">
        <label>Email:</label>
        <input type="email" v-model="email" placeholder="example@mail.ru" />
      </div>
      <div class="form_item">
        <label>Пароль:</label>
        <input
          type="password"
          v-model="password"
          placeholder="Придумайте пароль"
        />
      </div>
      <p class="error_text" v-if="error">{{ error }}</p>
      <div class="buttons_row">
        <button @click="Post_Register">Зарегистрироваться</button>
        <button class="secondary_btn" @click="$emit('emit_to_login')">
          Назад
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { Axios_Post } from "../index.js";

export default {
  data() {
    return {
      first_name: "",
      last_name: "",
      email: "",
      password: "",
      error: "",
    };
  },
  methods: {
    async Post_Register() {
      if (this.email == "" || this.password == "" || this.first_name == "") {
        this.error = "Заполните обязательные поля";
        return;
      }
      try {
        await Axios_Post("/register", {
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email,
          password: this.password,
        });
        alert("Регистрация успешна! Теперь войдите.");
        this.$emit("emit_register_success");
        this.first_name = "";
        this.last_name = "";
        this.email = "";
        this.password = "";
        this.error = "";
      } catch (e) {
        this.error = e.response?.data?.message || "Ошибка регистрации";
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
  margin-top: 50px;
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
