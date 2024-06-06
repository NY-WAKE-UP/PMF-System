<template>
  <div>
    <SiteNavigation/>
    <Menu/>
    <div class="hero min-h-screen bg-cover bg-center"
         style="background-image: url(https://img.daisyui.com/images/stock/photo-1507358522600-9f71e620c44e.jpg);">
      <div class="hero-overlay bg-black bg-opacity-50"></div>
      <div class="container mx-auto py-12">
        <div class="text-center mb-6 text-white">
          <h1 class="text-3xl font-semibold">Search Results for "{{ searchQuery }}"</h1>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          <div v-for="(movie, index) in movielist" :key="index">
            <div class="card bg-base-100 shadow-xl rounded-lg overflow-hidden ">
              <img :src="movie.img_url" alt="Movie" class="w-full h-64 object-cover">
              <div class="card-body p-4 ">
                <h2 class="text-lg font-semibold text-primary mb-2">{{ movie.movie_title }}</h2>
                <div class="flex items-center justify-between text-sm text-gray-500 mb-2">
                  <span>{{ movie.year }}</span>
                  <span @click="goToGenre(movie.genre)"
                        class="btn btn-xs">{{ movie.genre }}</span>
                </div>
                <div class="flex justify-between items-center mb-2">
                  <button class="btn btn-xs text-sm flex items-center">
                    Rating:
                    <div class="badge badge-secondary badge-sm">{{ movie.movie_rating }}</div>
                  </button>
                  <button class="btn btn-circle btn-sm" @click="goToDetails(movie.movie_id)"> ></button>
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
      searchQuery: this.$route.query.q || ""
    };
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
    },
    async fetchSearchResults() {
      try {
        const response = await axios.get(`http://localhost:8000/movies/search/${this.searchQuery}`);
        this.movielist = response.data;
        sessionStorage.setItem('searchResults', JSON.stringify(this.movielist));
      } catch (error) {
        console.error('Error fetching search results:', error);
      }
    }
  },
  created() {
    const storedResults = sessionStorage.getItem('searchResults');
    if (storedResults && this.searchQuery === this.$route.query.q) {
      this.movielist = JSON.parse(storedResults);
    } else {
      this.fetchSearchResults();
    }
  },
  watch: {
    '$route.query.q': {
      immediate: true,
      handler(newQuery) {
        this.searchQuery = newQuery;
        this.fetchSearchResults();
      }
    }
  }
};
</script>

<style scoped>
.text-primary {
  color: #00bcd4;
}

.card {
  position: relative;
}

.btn-circle {
  margin-left: 10px;
}

.card:hover {
  transform: translateY(-4px);
}
</style>
