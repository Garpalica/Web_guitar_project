<template>
  <div class="main_all_songs">
    <div class="header_block">
      <h1>Каталог песен</h1>
      <div class="buttons_filter">
        <button class="text_button" @click="Sort_songs('new')">
          Сначала новые
        </button>
        <button class="text_button" @click="Sort_songs('old')">
          Сначала старые
        </button>
        <button class="text_button" @click="Sort_songs('popular')">
          Популярные
        </button>
      </div>
    </div>
    <div class="filters-panel">
      <div class="search-box">
        <input type="password" style="display: none" />
        <input
          type="search"
          v-model="filters.search"
          @input="ApplyFilters"
          placeholder="Поиск по названию или исполнителю..."
          name="search_unq_random_field"
          autocomplete="off"
        />
      </div>
      <div class="select-filters">
        <select v-model="filters.tonality" @change="ApplyFilters">
          <option value="">Все тональности</option>
          <option v-for="t in tonalities_list" :key="t" :value="t">
            {{ t }}
          </option>
        </select>
        <select v-model="filters.genre" @change="ApplyFilters">
          <option value="">Все жанры</option>
          <option v-for="g in genres_list" :key="g" :value="g">{{ g }}</option>
        </select>
        <select v-model="filters.strumming" @change="ApplyFilters">
          <option value="">Все бои</option>
          <option v-for="s in strumming_list" :key="s" :value="s">
            {{ s }}
          </option>
        </select>
        <button class="reset-btn" @click="ResetFilters">Сбросить</button>
      </div>
    </div>
    <div class="list_songs">
      <div class="song_card" v-for="el in list_songs" :key="el.id">
        <div class="card-header">
          <h2>{{ el.title }}</h2>
          <span class="genre-tag">{{ el.genre }}</span>
        </div>
        <p class="artist-line">
          Исполнитель: <b>{{ el.artist }}</b>
        </p>

        <div class="rating_block">
          <span class="rating_text">Оценка: {{ el.rating || 0 }}</span>
          <div class="stars_row">
            <span
              v-for="star in 5"
              :key="star"
              class="star_icon"
              :class="{ filled: star <= Math.round(el.rating || 0) }"
              @click="Rate_song(el.id, star)"
              title="Поставить оценку"
            >
              ★
            </span>
          </div>
        </div>

        <div class="tags-row">
          <span class="info-tag">{{ el.tonality }}</span>
          <span class="info-tag">{{ el.strumming_pattern }}</span>
        </div>
        <p class="author-text">Добавил: {{ el.added_by }}</p>
        <button class="view-btn" @click="Emit_show_one_song(el)">
          Смотреть аккорды
        </button>
      </div>
      <p v-if="list_songs.length === 0" style="margin-top: 20px; color: gray">
        Ничего не найдено...
      </p>
    </div>
  </div>
</template>

<script>
import { Axios_Get, Axios_Post } from "../index.js";
import { TONALITIES, GENRES, STRUMMING_PATTERNS } from "../constants.js";

export default {
  data() {
    return {
      list_songs: [],
      original_full_songs: [],
      tonalities_list: TONALITIES,
      genres_list: GENRES,
      strumming_list: STRUMMING_PATTERNS,
      filters: { search: "", tonality: "", genre: "", strumming: "" },
    };
  },
  async mounted() {
    await this.Get_songs();
  },
  methods: {
    async Get_songs() {
      try {
        const response = await Axios_Get("/songs");
        this.original_full_songs = response.data.songs;
        this.list_songs = [...this.original_full_songs];
        this.Sort_songs("new");
      } catch (e) {
        console.log(e);
      }
    },

    async Rate_song(song_id, value) {
      try {
        await Axios_Post("/rate", {
          song_id: song_id,
          value: value,
        });
        await this.Get_songs();
      } catch (e) {
        alert("Чтобы голосовать, нужно войти в аккаунт!");
      }
    },

    Sort_songs(type) {
      if (type === "new") {
        this.list_songs.sort((a, b) => b.id - a.id);
      } else if (type === "old") {
        this.list_songs.sort((a, b) => a.id - b.id);
      } else if (type === "popular") {
        this.list_songs.sort((a, b) => (b.rating || 0) - (a.rating || 0));
      }
    },

    ApplyFilters() {
      let result = this.original_full_songs;
      if (this.filters.search) {
        const query = this.filters.search.toLowerCase();
        result = result.filter(
          (song) =>
            song.title.toLowerCase().includes(query) ||
            song.artist.toLowerCase().includes(query),
        );
      }
      if (this.filters.tonality)
        result = result.filter(
          (song) => song.tonality === this.filters.tonality,
        );
      if (this.filters.genre)
        result = result.filter((song) => song.genre === this.filters.genre);
      if (this.filters.strumming)
        result = result.filter(
          (song) => song.strumming_pattern === this.filters.strumming,
        );
      this.list_songs = result;
    },
    ResetFilters() {
      this.filters.search = "";
      this.filters.tonality = "";
      this.filters.genre = "";
      this.filters.strumming = "";
      this.list_songs = [...this.original_full_songs];
    },
    Emit_show_one_song(el) {
      this.$emit("emit_show_one_song", el);
    },
  },
};
</script>

<style scoped>
.header_block {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
h1 {
  margin-bottom: 10px;
}
.filters-panel {
  background-color: white;
  padding: 15px;
  border-radius: 10px;
  margin-top: 15px;
  border: 1px solid #ddd;
  width: 100%;
  box-sizing: border-box;
}
.search-box input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-bottom: 15px;
  box-sizing: border-box;
  font-size: 16px;
}
.select-filters {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
select {
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  flex-grow: 1;
}
.reset-btn {
  background-color: #ddd;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
}
.list_songs {
  margin-top: 20px;
  width: 100%;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
.song_card {
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 15px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
  box-sizing: border-box;
}
.song_card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}
.card-header h2 {
  margin: 0;
  font-size: 1.3em;
  word-break: break-word;
}
.genre-tag {
  background-color: #e1bee7;
  font-size: 0.8em;
  padding: 2px 8px;
  border-radius: 10px;
  white-space: nowrap;
  margin-left: 5px;
  height: fit-content;
}
.rating_block {
  margin: 5px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.stars_row {
  font-size: 24px;
  cursor: pointer;
}
.star_icon {
  color: #ccc;
  transition: color 0.2s;
}
.star_icon.filled {
  color: #ffc107;
}
.star_icon:hover {
  color: #ffdb70;
}
.rating_text {
  font-size: 0.9em;
  font-weight: bold;
  color: #555;
}
.tags-row {
  display: flex;
  gap: 5px;
  margin: 10px 0;
  flex-wrap: wrap;
}
.info-tag {
  background-color: #bbdefb;
  font-size: 0.9em;
  padding: 4px 8px;
  border-radius: 5px;
}
.author-text {
  font-size: 0.8em;
  color: gray;
  margin-bottom: 15px;
  margin-top: auto;
}
.buttons_filter button {
  margin: 5px;
  padding: 8px 15px;
  cursor: pointer;
  background: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
}
.view-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  width: 100%;
}
@media (max-width: 1100px) {
  .list_songs {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 700px) {
  .list_songs {
    grid-template-columns: 1fr;
  }
}
</style>
