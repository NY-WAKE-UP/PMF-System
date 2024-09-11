<template>
  <div>
    <SiteNavigation/>
    <Menu/>
    <div class="hero min-h-screen bg-cover bg-center"
         style="background-image: url(https://img.daisyui.com/images/stock/photo-1507358522600-9f71e620c44e.webp);">
      <div class="hero-overlay bg-black bg-opacity-50"></div>
      <div class="container mx-auto py-12">
        <div class="text-center text-white mb-6">
          <h1 class="text-3xl font-semibold">{{ genre }} Movies</h1>
          <p class="text-lg">您好 这是当前为您找到的所有 {{ genre }} 类型的电影</p>
        </div>
        <div v-if="loading" class="text-center text-white mb-6">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline-block" xmlns="http://www.w3.org/2000/svg"
               fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Loading...
        </div>
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          <div v-for="(movie, index) in movielist" :key="index">
            <div class="card bg-base-100 shadow-xl rounded-lg overflow-hidden">
              <img :src="movie.img_url" alt="Movie" class="w-full h-64 object-cover">
              <div class="card-body p-4">
                <h2 class="text-lg font-semibold text-primary mb-2">{{ movie.movie_title }}</h2>
                <div class="flex items-center justify-between text-sm text-gray-500 mb-2">
                  <span>{{ movie.year }}</span>
                  <span @click="goToGenre(movie.genre)"
                        class="cursor-pointer text-blue-500 hover:underline">{{ movie.genre }}</span>
                </div>
                <div class="flex justify-between items-center mb-2">
                  <button class="btn btn-xs text-sm flex items-center">
                    Rating:
                    <div class="badge badge-secondary badge-sm">{{ movie.movie_rating }}</div>
                  </button>
                  <button class="btn btn-circle btn-sm" @click="goToDetails(movie.movie_id)">></button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SiteNavigation from "@/components/SiteNavigation.vue";
import Menu from "@/components/Menu.vue";
import axios from "axios";

export default {
  data() {
    return {
      movielist: [],
      genre: this.$route.params.genre,
      loading: true
    }
  },
  created() {
    axios.get(`http://localhost:8000/movies/genre/${this.genre}`)
        .then(response => {
          this.movielist = response.data;
          this.loading = false;
        })
        .catch(error => {
          console.error('Error fetching movies by genre:', error);
          this.loading = false;
        });
  },
  components: {
    SiteNavigation,
    Menu
  },
  methods: {
    goToDetails(movieId) {
      this.$router.push({name: 'details', params: {movieId}});
    },
    goToGenre(genre) {
      this.$router.push({name: 'genreMovies', params: {genre}});
    }
  }
}
</script>

<style scoped>
.text-primary {
  color: #00bcd4;
}

.btn-circle {
  margin-left: 10px;
}

.card {
  position: relative;
}

.card:hover {
  transform: translateY(-4px);
}
</style>
