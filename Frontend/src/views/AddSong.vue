<template>
  <div class="add_song_container">
    <h1>Добавить песню</h1>
    <div class="form_group">
      <label>Название:</label>
      <input v-model="title" placeholder="Например: Кукушка" />
    </div>
    <div class="form_group">
      <label>Исполнитель:</label>
      <input v-model="artist" placeholder="Например: Кино" />
    </div>
    <div class="dropdowns_row">
      <div class="form_group half">
        <label>Тональность:</label>
        <select v-model="tonality">
          <option disabled value="">Выберите...</option>
          <option v-for="t in tonalities_list" :key="t" :value="t">
            {{ t }}
          </option>
        </select>
      </div>
      <div class="form_group half">
        <label>Жанр:</label>
        <select v-model="genre">
          <option disabled value="">Выберите...</option>
          <option v-for="g in genres_list" :key="g" :value="g">{{ g }}</option>
        </select>
      </div>
      <div class="form_group half">
        <label>Бой:</label>
        <select v-model="strumming_pattern">
          <option disabled value="">Выберите...</option>
          <option v-for="s in strumming_list" :key="s" :value="s">
            {{ s }}
          </option>
        </select>
      </div>
    </div>
    <div class="form_group">
      <label>Текст с аккордами:</label>
      <div class="chord-helper">
        <span>Вставить: </span>
        <div class="chord-buttons-wrapper">
          <button
            v-for="chord in chords_helper"
            :key="chord"
            class="chord-btn"
            @click="InsertChord(chord)"
          >
            {{ chord }}
          </button>
        </div>
      </div>
      <textarea
        ref="songTextarea"
        v-model="text"
        placeholder="Напишите текст..."
      ></textarea>
    </div>
    <div class="buttons-row">
      <button class="main-btn" @click="Create_song">Создать</button>
      <button class="main-btn cancel-btn" @click="$emit('emit_back_to_list')">
        Отмена
      </button>
    </div>
  </div>
</template>

<script>
import { Axios_Post } from "../index.js";
import {
  TONALITIES,
  GENRES,
  STRUMMING_PATTERNS,
  CHORDS_HELPER,
} from "../constants.js";

export default {
  data() {
    return {
      title: "",
      artist: "",
      tonality: "",
      genre: "",
      strumming_pattern: "",
      text: "",
      tonalities_list: TONALITIES,
      genres_list: GENRES,
      strumming_list: STRUMMING_PATTERNS,
      chords_helper: CHORDS_HELPER,
    };
  },
  methods: {
    InsertChord(chord) {
      const textarea = this.$refs.songTextarea;
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const text = this.text;
      const insertText = `[${chord}]`;
      this.text = text.substring(0, start) + insertText + text.substring(end);
      this.$nextTick(() => {
        textarea.focus();
        textarea.setSelectionRange(
          start + insertText.length,
          start + insertText.length,
        );
      });
    },
    async Create_song() {
      if (
        !this.title ||
        !this.text ||
        !this.tonality ||
        !this.genre ||
        !this.strumming_pattern
      ) {
        alert("Заполните все поля!");
        return;
      }
      try {
        await Axios_Post("/songs", {
          title: this.title,
          artist: this.artist,
          tonality: this.tonality,
          genre: this.genre,
          strumming_pattern: this.strumming_pattern,
          text_with_chords: this.text,
        });
        alert("Песня добавлена!");
        this.title = "";
        this.artist = "";
        this.tonality = "";
        this.text = "";
        this.genre = "";
        this.strumming_pattern = "";
        this.$emit("emit_back_to_list");
      } catch (e) {
        alert("Ошибка: " + (e.response?.data?.message || e.message));
      }
    },
  },
};
</script>

<style scoped>
.add_song_container {
  width: 100%;
  margin: 30px auto;
  padding: 20px;
  border: 2px solid steelblue;
  border-radius: 15px;
  background-color: white;
  box-sizing: border-box;
}
.form_group {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
}
label {
  margin-bottom: 5px;
  font-weight: bold;
}
input,
select {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
  box-sizing: border-box;
}
.dropdowns_row {
  display: flex;
  gap: 20px;
  justify-content: space-between;
}
.half {
  flex: 1;
}
.chord-helper {
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f0f8ff;
  border-radius: 5px;
  border: 1px dashed #ccc;
}
.chord-buttons-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 5px;
}
.chord-btn {
  width: auto !important;
  background-color: white;
  border: 1px solid #aaa;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 4px;
  font-weight: bold;
  font-size: 14px;
  flex: 0 0 auto;
  transition: background 0.2s;
}
.chord-btn:hover {
  background-color: #e3f2fd;
  border-color: #2196f3;
}
textarea {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
  box-sizing: border-box;
  resize: vertical;
  min-height: 250px;
  font-family: monospace;
}
.buttons-row {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}
.main-btn {
  padding: 12px 20px;
  cursor: pointer;
  font-size: 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  width: 100%;
}
.cancel-btn {
  background-color: #f44336;
}
@media (max-width: 600px) {
  .dropdowns_row {
    flex-direction: column;
    gap: 0;
  }
}
</style>
