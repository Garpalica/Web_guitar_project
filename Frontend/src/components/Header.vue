<template>
  <header class="header">
    <div class="logo" @click="$emit('emit_show_main_page')">GuitarSongs</div>
    <nav class="nav-buttons">
      <div v-if="user_name" class="user-menu">
        <span class="welcome-text"
          >Привет, <b>{{ user_name }}</b
          >!</span
        >
        <button class="nav-btn" @click="$emit('emit_show_add_song')">
          Добавить песню
        </button>
        <button class="logout-btn" @click="$emit('emit_logout')">Выйти</button>
      </div>
      <div v-else class="guest-menu">
        <button class="nav-btn" @click="$emit('emit_show_login_page')">
          Вход
        </button>
        <button class="nav-btn" @click="$emit('emit_show_register_page')">
          Регистрация
        </button>
      </div>
    </nav>
  </header>
</template>

<script>
export default { props: ["user_name"] };
</script>

<style scoped>
.header {
  background-color: #333;
  color: white;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
  border-radius: 0 0 10px 10px;
  margin-bottom: 20px;
}
.logo {
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  white-space: nowrap;
}
.nav-buttons {
  display: flex;
  width: auto;
}
.user-menu,
.guest-menu {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.nav-btn {
  background: transparent;
  border: 1px solid white;
  color: white;
  padding: 8px 15px;
  cursor: pointer;
  border-radius: 5px;
  white-space: nowrap;
}
.nav-btn:hover {
  background-color: white;
  color: #333;
}
.logout-btn {
  background-color: #ff4d4d;
  border: none;
  color: white;
  padding: 8px 15px;
  cursor: pointer;
  border-radius: 5px;
}
.welcome-text {
  white-space: nowrap;
}
@media (max-width: 600px) {
  .header {
    flex-direction: column;
  }
  .nav-buttons {
    justify-content: center;
    width: 100%;
  }
}
</style>
