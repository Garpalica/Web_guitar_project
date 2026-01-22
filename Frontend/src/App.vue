<template>
  <div class="app-container">
    <Header
      :user_name="user_name"
      @emit_show_main_page="Show_song_list"
      @emit_show_login_page="show = 'login_page'"
      @emit_show_register_page="show = 'register_page'"
      @emit_show_add_song="show = 'add_song_page'"
      @emit_logout="Logout"
    ></Header>

    <SongList
      v-show="show == 'song_list'"
      ref="Load_list"
      @emit_show_one_song="Show_Detail"
    ></SongList>

    <SongDetail
      v-show="show == 'detail_page'"
      :song_data="current_song"
      :user_name="user_name"
      :user_id="user_id"
      @emit_back_to_list="Show_song_list"
    ></SongDetail>

    <AddSong
      v-show="show == 'add_song_page'"
      @emit_back_to_list="Show_song_list"
    ></AddSong>

    <Login
      v-show="show == 'login_page'"
      @emit_login_success="Data_user"
      @emit_to_register="show = 'register_page'"
    ></Login>

    <Register
      v-show="show == 'register_page'"
      @emit_register_success="show = 'login_page'"
      @emit_to_login="show = 'login_page'"
    ></Register>
  </div>
</template>

<script>
import SongList from "./views/SongList.vue";
import SongDetail from "./views/SongDetail.vue";
import AddSong from "./views/AddSong.vue";
import Login from "./views/Login.vue";
import Register from "./views/Register.vue";
import Header from "./components/Header.vue";
import { Axios_Get } from "./index.js";

export default {
  components: { SongList, SongDetail, AddSong, Login, Register, Header },
  data() {
    return {
      show: "song_list",
      current_song: {},
      user_name: "",
      user_id: "",
    };
  },
  mounted() {
    const storedUserName = localStorage.getItem("user_name");
    const storedUserId = localStorage.getItem("user_id");
    if (storedUserName && storedUserId) {
      this.user_name = storedUserName;
      this.user_id = storedUserId;
      this.show = "song_list";
    }
  },
  methods: {
    Show_song_list() {
      this.show = "song_list";
      this.current_song = {};
      if (this.$refs.Load_list) {
        this.$refs.Load_list.Get_songs();
      }
    },
    Show_Detail(el) {
      this.current_song = el;
      this.show = "detail_page";
    },
    Data_user(name, id) {
      this.user_name = name;
      this.user_id = id;
      localStorage.setItem("user_name", name);
      localStorage.setItem("user_id", id);
      this.Show_song_list();
    },
    async Logout() {
      await Axios_Get("/logout");
      this.user_name = "";
      this.user_id = "";
      localStorage.clear();
      this.show = "login_page";
      window.location.reload();
    },
  },
};
</script>
<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f8f9fa;
}
.app-container {
  width: 100%;
  padding: 0 20px;
  box-sizing: border-box;
}
</style>
