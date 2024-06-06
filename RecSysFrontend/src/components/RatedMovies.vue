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
          <p class="text-lg"> 曾评分过的电影（根据您的评分值由高到低排序）</p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          <div v-for="(movie,index) in movielist" :key="index">
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
        <p class="text-center text-white mt-6">以上是 {{ username }} 曾评分过的电影</p>
      </div>
    </div>
  </div>
</template>

<script>
import SiteNavigation from "@/components/SiteNavigation.vue";
import Menu from "@/components/Menu.vue";
import axios from "axios";

export default {
  name: "Profile",
  components: {Menu, SiteNavigation},
  data() {
    return {
      movielist: [],
      user_id: sessionStorage.getItem('user_id'),
      username: sessionStorage.getItem('username')
    }
  },
  created() {
    axios.get(`http://localhost:8000/movies/rated/${this.user_id}`)
        .then(response => {
          this.movielist = response.data;
        })
        .catch(error => {
          console.error('Error fetching recommended movies:', error);
        });
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

<style scoped lang="scss">
/* 你可以在这里添加一些自定义的样式 */
</style>
