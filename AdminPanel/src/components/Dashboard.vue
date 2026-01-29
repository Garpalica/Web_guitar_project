<template>
  <div class="dashboard">
    <div class="header">
      <h1>Админ Панель</h1>
      <button @click="logout" class="logout-btn">Выйти</button>
    </div>

    <div class="tabs">
      <button
        @click="currentTab = 'users'"
        :class="{ active: currentTab === 'users' }"
      >
        Пользователи
      </button>
      <button
        @click="currentTab = 'songs'"
        :class="{ active: currentTab === 'songs' }"
      >
        Песни
      </button>
      <button
        @click="currentTab = 'comments'"
        :class="{ active: currentTab === 'comments' }"
      >
        Комментарии
      </button>
    </div>

    <div class="content">
      <div v-if="currentTab === 'users'">
        <h3>Все пользователи</h3>
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Email</th>
              <th>Имя</th>
              <th>Роль</th>
              <th>Действие</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td>{{ u.id }}</td>
              <td>{{ u.email }}</td>
              <td>{{ u.first_name }}</td>
              <td>
                <span
                  :class="u.role === 'admin' ? 'badge-admin' : 'badge-user'"
                >
                  {{ u.role }}
                </span>
              </td>
              <td>
                <button
                  v-if="u.role !== 'admin'"
                  @click="changeRole(u.id, 'admin')"
                >
                  Сделать Админом
                </button>
                <button v-else @click="changeRole(u.id, 'user')">
                  Разжаловать
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="currentTab === 'songs'">
        <h3>Все разборы</h3>
        <div v-for="song in songs" :key="song.id" class="item-row">
          <div>
            <strong>{{ song.title }}</strong> — {{ song.artist }} <br />
            <small>Добавил: {{ song.added_by }}</small>
          </div>
          <button @click="deleteSong(song.id)" class="btn-delete">
            Удалить
          </button>
        </div>
      </div>

      <div v-if="currentTab === 'comments'">
        <h3>Управление комментариями</h3>
        <p v-if="songs.length === 0">Сначала загрузите песни...</p>

        <div v-for="song in songs" :key="song.id">
          <div class="comment-section">
            <strong>{{ song.artist }} - {{ song.title }}</strong>
            <button @click="loadComments(song.id)">Показать комменты</button>

            <div v-if="comments[song.id]" class="comments-list">
              <div
                v-for="c in comments[song.id]"
                :key="c.id"
                class="comment-row"
              >
                <span>
                  <b>{{ c.author_name }}:</b> {{ c.text }}
                </span>
                <button
                  @click="deleteComment(c.id, song.id)"
                  class="btn-delete-small"
                >
                  X
                </button>
              </div>
              <div v-if="comments[song.id].length === 0" style="color: gray">
                Нет комментариев
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Axios_Get, Axios_Put, Axios_Delete } from "../index.js";

export default {
  data() {
    return {
      currentTab: "users",
      users: [],
      songs: [],
      comments: {},
    };
  },
  methods: {
    async fetchData() {
      try {
        const uRes = await Axios_Get("/admin/users");
        this.users = uRes.data.users;

        const sRes = await Axios_Get("/songs");
        this.songs = sRes.data.songs;
      } catch (e) {
        console.error(e);
        if (e.response && e.response.status === 403) {
          this.logout();
        }
      }
    },
    async changeRole(uid, role) {
      try {
        await Axios_Put("/admin/users", { user_id: uid, new_role: role });
        this.fetchData();
      } catch (e) {
        alert("Ошибка смены роли");
      }
    },
    async deleteSong(id) {
      if (!confirm("Удалить песню?")) return;
      try {
        await Axios_Delete(`/admin/songs/${id}`);
        this.fetchData();
      } catch (e) {
        alert("Ошибка удаления");
      }
    },
    async loadComments(songId) {
      try {
        const res = await Axios_Get(`/comments?song_id=${songId}`);
        this.comments[songId] = res.data.comments;
      } catch (e) {
        console.log(e);
      }
    },
    async deleteComment(commentId, songId) {
      if (!confirm("Удалить комментарий?")) return;
      try {
        await Axios_Delete(`/admin/comments/${commentId}`);
        this.loadComments(songId);
      } catch (e) {
        alert("Ошибка удаления комментария");
      }
    },
    async logout() {
      try {
        await Axios_Get("/logout");
        this.$emit("logout");
      } catch (e) {
        this.$emit("logout");
      }
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style scoped>
.dashboard {
  background: white;
  padding: 20px;
  min-height: 80vh;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  margin-bottom: 20px;
}
.tabs {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}
.tabs button {
  padding: 10px 20px;
  background: #e0e0e0;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}
.tabs button.active {
  background: #333;
  color: white;
}
.data-table {
  width: 100%;
  border-collapse: collapse;
}
.data-table th,
.data-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
.badge-admin {
  color: red;
  font-weight: bold;
}
.badge-user {
  color: green;
}
.item-row {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #eee;
  align-items: center;
}
.btn-delete {
  background: #ff4444;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 4px;
}
.comment-section {
  margin-top: 10px;
  padding: 10px;
  background: #f9f9f9;
  border-left: 3px solid #333;
}
.comments-list {
  margin-top: 10px;
  margin-left: 20px;
}
.comment-row {
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #ddd;
  padding: 5px 0;
}
.btn-delete-small {
  background: red;
  color: white;
  border: none;
  cursor: pointer;
  padding: 2px 6px;
  font-size: 12px;
  border-radius: 3px;
}
</style>
