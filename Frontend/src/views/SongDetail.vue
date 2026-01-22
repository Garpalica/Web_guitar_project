<template>
  <div class="main_page_detail">
    <div class="song_detail_card" v-if="full_song && editor_song == null">
      <div class="detail-header">
        <h1>{{ full_song.title }}</h1>
        <span class="big-genre-tag">{{ full_song.genre }}</span>
      </div>
      <h3>Исполнитель: {{ full_song.artist }}</h3>
      <div class="info-grid">
        <p>
          Тональность: <b>{{ full_song.tonality }}</b>
        </p>
        <p>
          Бой: <b>{{ full_song.strumming_pattern }}</b>
        </p>
        <p>Добавил: {{ full_song.added_by }}</p>
      </div>
      <pre class="chords_text">{{ full_song.text_with_chords }}</pre>
      <div class="buttons_detail" v-if="Is_Author()">
        <button
          type="button"
          class="del-btn"
          @click="Delete_song(full_song.id)"
        >
          Удалить песню
        </button>
        <button type="button" class="edit-btn" @click="Editor_song_start">
          Редактировать
        </button>
      </div>
      <button
        type="button"
        id="tip"
        @click="Emit_back_to_list"
        class="back-btn"
      >
        Вернуться к списку
      </button>
    </div>
    <div v-else-if="!full_song && song_data" class="song_detail_card">
      <h3>Загрузка...</h3>
    </div>
    <div
      class="song_detail_card"
      v-if="full_song && editor_song == full_song.id"
    >
      <h2>Редактирование</h2>
      <div class="edit-form">
        <label>Название:</label> <input type="text" v-model="new_song_title" />
        <label>Исполнитель:</label>
        <input type="text" v-model="new_song_artist" />
        <div class="edit-row">
          <div>
            <label>Тональность:</label
            ><select v-model="new_song_tonality">
              <option v-for="t in tonalities_list" :key="t" :value="t">
                {{ t }}
              </option>
            </select>
          </div>
          <div>
            <label>Жанр:</label
            ><select v-model="new_song_genre">
              <option v-for="g in genres_list" :key="g" :value="g">
                {{ g }}
              </option>
            </select>
          </div>
          <div>
            <label>Бой:</label
            ><select v-model="new_song_strumming">
              <option v-for="s in strumming_list" :key="s" :value="s">
                {{ s }}
              </option>
            </select>
          </div>
        </div>
        <label>Текст:</label>
        <textarea v-model="new_song_text" rows="15"></textarea>
      </div>
      <div class="buttons_detail">
        <button @click="Put_song(full_song.id)">Сохранить</button>
        <button class="cancel-btn" @click="editor_song = null">Отмена</button>
      </div>
    </div>
    <div class="comment_card" v-if="full_song">
      <div class="comment_title">
        <h2>Комментарии:</h2>
        <div v-if="user_id" style="display: flex; gap: 10px; flex-wrap: wrap">
          <input
            class="input_class"
            placeholder="Ваш комментарий..."
            type="text"
            v-model="new_comment_text"
          />
          <button type="button" @click="Post_Comment">Отправить</button>
        </div>
        <div v-else>
          <p><i>Войдите, чтобы оставить комментарий</i></p>
        </div>
      </div>
      <div class="comments_list">
        <div class="comment_item" v-for="comm in comments" :key="comm.id">
          <div v-if="editor_comment != comm.id">
            <p>
              <b>{{ comm.author_name }}</b>
              <span style="font-size: 0.8em; color: gray">{{ comm.date }}</span>
            </p>
            <p>{{ comm.text }}</p>
            <div v-if="comm.user_id == user_id" class="comm-actions">
              <button class="small-btn del" @click="Delete_comment(comm.id)">
                Удалить
              </button>
              <button class="small-btn" @click="Start_edit_comment(comm)">
                Изменить
              </button>
            </div>
          </div>
          <div v-else>
            <input
              type="text"
              v-model="edit_comment_text"
              style="width: 100%; margin-bottom: 5px"
            />
            <button class="small-btn" @click="Put_comment(comm.id)">
              Сохранить
            </button>
            <button class="small-btn del" @click="editor_comment = null">
              Отмена
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Axios_Get, Axios_Post, Axios_Put, Axios_Delete } from "../index.js";
import { TONALITIES, GENRES, STRUMMING_PATTERNS } from "../constants.js";

export default {
  data() {
    return {
      full_song: null,
      comments: [],
      new_comment_text: "",
      edit_comment_text: "",
      editor_comment: null,
      editor_song: null,
      new_song_title: "",
      new_song_artist: "",
      new_song_tonality: "",
      new_song_text: "",
      new_song_genre: "",
      new_song_strumming: "",
      tonalities_list: TONALITIES,
      genres_list: GENRES,
      strumming_list: STRUMMING_PATTERNS,
    };
  },
  props: { song_data: Object, user_name: String, user_id: [String, Number] },
  watch: {
    song_data: {
      handler(newVal) {
        if (newVal?.id) {
          this.full_song = null;
          this.Get_Full_Song(newVal.id);
          this.Get_comments(newVal.id);
        }
      },
      immediate: true,
    },
  },
  methods: {
    async Get_Full_Song(id) {
      try {
        const res = await Axios_Get("/songs/" + id);
        this.full_song = res.data;
      } catch (e) {
        alert("Ошибка загрузки");
      }
    },
    Emit_back_to_list() {
      this.$emit("emit_back_to_list");
      this.editor_song = null;
    },
    Is_Author() {
      return this.full_song && this.full_song.added_by_id == this.user_id;
    },
    async Delete_song(id) {
      if (confirm("Удалить?")) {
        await Axios_Delete("/songs", { id });
        this.Emit_back_to_list();
      }
    },
    Editor_song_start() {
      this.editor_song = this.full_song.id;
      this.new_song_title = this.full_song.title;
      this.new_song_artist = this.full_song.artist;
      this.new_song_tonality = this.full_song.tonality;
      this.new_song_text = this.full_song.text_with_chords;
      this.new_song_genre = this.full_song.genre;
      this.new_song_strumming = this.full_song.strumming_pattern;
    },
    async Put_song(id) {
      await Axios_Put("/songs", {
        id,
        title: this.new_song_title,
        artist: this.new_song_artist,
        tonality: this.new_song_tonality,
        genre: this.new_song_genre,
        strumming_pattern: this.new_song_strumming,
        text_with_chords: this.new_song_text,
      });
      this.full_song.title = this.new_song_title;
      this.full_song.artist = this.new_song_artist;
      this.full_song.tonality = this.new_song_tonality;
      this.full_song.genre = this.new_song_genre;
      this.full_song.strumming_pattern = this.new_song_strumming;
      this.full_song.text_with_chords = this.new_song_text;
      this.editor_song = null;
    },
    async Get_comments(id) {
      const res = await Axios_Get(`/comments?song_id=${id}`);
      this.comments = res.data.comments;
    },
    async Post_Comment() {
      if (!this.new_comment_text) return;
      await Axios_Post("/comments", {
        song_id: this.full_song.id,
        text: this.new_comment_text,
      });
      this.Get_comments(this.full_song.id);
      this.new_comment_text = "";
    },
    async Delete_comment(id) {
      await Axios_Delete("/comments", { id });
      this.Get_comments(this.full_song.id);
    },
    Start_edit_comment(comm) {
      this.editor_comment = comm.id;
      this.edit_comment_text = comm.text;
    },
    async Put_comment(id) {
      await Axios_Put("/comments", { id, text: this.edit_comment_text });
      this.editor_comment = null;
      this.Get_comments(this.full_song.id);
    },
  },
};
</script>

<style scoped>
.chords_text {
  background-color: #f0f0f0;
  padding: 15px;
  border-radius: 5px;
  font-family: monospace;
  white-space: pre-wrap;
  margin-top: 15px;
  color: #333;
  overflow-x: auto;
}
.song_detail_card {
  width: 100%;
  margin: 0 auto 20px auto;
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #ccc;
  box-sizing: border-box;
}
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
  flex-wrap: wrap;
  gap: 10px;
}
.detail-header h1 {
  margin: 0;
  font-size: 1.5em;
  word-break: break-word;
}
.big-genre-tag {
  background-color: #8e24aa;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}
.info-grid {
  display: flex;
  gap: 20px;
  background: #fafafa;
  padding: 10px;
  border-radius: 5px;
  margin-top: 10px;
  flex-wrap: wrap;
}
.info-grid p {
  margin: 0;
}
.buttons_detail {
  margin-top: 15px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
button {
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 5px;
  border: none;
  font-size: 14px;
  color: white;
  background-color: #4caf50;
}
.del-btn,
.del {
  background-color: #ff5252;
}
.edit-btn {
  background-color: #2196f3;
}
.cancel-btn {
  background-color: #999;
}
.back-btn {
  margin-top: 10px;
  background-color: #607d8b;
  width: 100%;
}
.edit-row {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}
.edit-row > div {
  flex: 1;
  min-width: 150px;
}
input,
select,
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  margin-bottom: 10px;
}
.comment_card {
  width: 100%;
  margin: 0 auto;
  background-color: aliceblue;
  padding: 20px;
  border-radius: 10px;
  box-sizing: border-box;
}
.input_class {
  flex: 1;
  margin-bottom: 0 !important;
}
.comment_item {
  background: white;
  padding: 10px;
  margin-top: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
}
.small-btn {
  padding: 5px 10px;
  font-size: 12px;
  margin-right: 5px;
}
</style>
