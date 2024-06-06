<script>
import Menu from "@/components/Menu.vue";
import axios from "axios";
import SiteNavigation from "@/components/SiteNavigation.vue";

export default {
  data() {
    return {
      movielist_for_recommend: [],
      user_id: sessionStorage.getItem('user_id'),
      username: sessionStorage.getItem('username'),
      loading: true
    }
  },
  created() {
    // 检查会话存储空间中是否存在 movielist
    const storedMovieList = sessionStorage.getItem('movielist_for_recommend');
    if (storedMovieList) {
      // 如果存在，则直接使用存储的 movielist
      this.movielist_for_recommend = JSON.parse(storedMovieList);
      this.loading = false
    } else {
      // 如果不存在，则发送请求获取 movielist，并存储到会话存储空间
      axios.get(`http://localhost:8000/movies/recommend/${this.user_id}`)
          .then(response => {
            this.movielist_for_recommend = response.data;
            // 存储到会话存储空间
            sessionStorage.setItem('movielist_for_recommend', JSON.stringify(response.data));
            console.log(this.movielist_for_recommend)
          })
          .catch(error => {
            console.error('Error fetching recommended movies:', error);
          })
          .finally(() => {
            this.loading = false; // 无论请求成功还是失败，最终都设置为 false
          });

    }
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

<template>
  <div>
    <SiteNavigation/>
    <Menu/>
    <div class="hero min-h-screen bg-cover bg-center"
         style="background-image: url(https://img.daisyui.com/images/stock/photo-1507358522600-9f71e620c44e.jpg);">
      <div class="hero-overlay bg-black bg-opacity-50"></div>
      <div class="container mx-auto py-12">
        <div class="text-center text-white mb-6">
          <h1 class="text-3xl font-semibold">{{ username }}</h1>
          <p class="text-lg"> 这是为您推荐的电影</p>
        </div>
        <div v-if="loading" class="flex justify-center items-center min-h-screen">
          <button type="button"
                  class="inline-flex items-center px-4 py-2 font-semibold leading-6 text-sm shadow rounded-md text-white  bg-emerald-700 hover:bg-emerald-600 transition ease-in-out duration-150 cursor-not-allowed"
                  disabled="" data-immersive-translate-walked="011e9135-83ef-4363-b3db-0b4ca6d2cc05"
                  data-immersive-translate-paragraph="1">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                 viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Loading...
          </button>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          <div v-for="(movie,index) in movielist_for_recommend" :key="index">
            <div class="card bg-base-100 shadow-xl rounded-lg overflow-hidden">
              <img :src="movie.img_url" alt="Movie" class="w-full h-64 object-cover">
              <div class="card-body p-4">
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
                  <div class="flex items-center">
                    <button class="btn btn-circle btn-sm mr-2" @click="goToDetails(movie.movie_id)"> ></button>
                  </div>

                </div>
              </div>

            </div>
          </div>
        </div>
        <p class="text-center text-white mt-6">以上是为 {{ username }} 推荐的电影</p>

      </div>
    </div>
  </div>
</template>

<style scoped>
.text-primary {
  color: #00bcd4;
}

.btn-circle {
  margin-left: 10px;
}

.card:hover {
  transform: translateY(-4px);
}

.animate-spin {
  animation: spin 1s linear infinite;

}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

</style>