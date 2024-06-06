<script>
import {ref, reactive, watch} from "vue";
import axios from "axios";
import {useRoute, useRouter} from "vue-router";
import Menu from "@/components/Menu.vue";
import SiteNavigation from "@/components/SiteNavigation.vue";

export default {
  components: {
    Menu,
    SiteNavigation,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const movielist = ref([]);
    const ratings = reactive({});
    const username = ref(sessionStorage.getItem("username") || "");

    const fetchMovies = async () => {
      try {
        const response = await axios.get("http://localhost:8000/movies/random");
        movielist.value = response.data;
        response.data.forEach(movie => {
          ratings[movie.movie_id] = movie.movie_rating;
        });
      } catch (error) {
        console.error('Error fetching popular movies:', error);
      }
    };

    const submitRating = async (movieId, newRating) => {
      try {
        const ratingResponse = await axios.post(
            "http://localhost:8000/movies/ratings",
            {
              movie_id: movieId,
              username: username.value,
              rating: newRating,
            }
        );
        console.log("Rating submitted successfully:", ratingResponse.data);
      } catch (error) {
        console.error("Error submitting rating:", error);
      }
    };

    const updateRating = (movieId, newRating) => {
      ratings[movieId] = newRating;
      submitRating(movieId, newRating);
    };


    fetchMovies();

    return {
      movielist,
      ratings,
      username,
      updateRating,
    };
  },
  methods: {
    goToDetails(movieId) {
      this.$router.push({name: 'details', params: {movieId}});
    },
    goToGenre(genre) {
      this.$router.push({name: 'genreMovies', params: {genre}});
    }
  }
};
</script>

<template>
  <SiteNavigation/>
  <Menu/>
  <div class="hero min-h-screen bg-cover bg-center"
       style="background-image: url(https://img.daisyui.com/images/stock/photo-1507358522600-9f71e620c44e.jpg);">
    <div class="hero-overlay bg-black bg-opacity-50"></div>
    <div class="container mx-auto py-12">
      <div class="text-center text-white mb-6">
        <h1 class="text-3xl font-semibold">{{ username }}</h1>
        <p class="text-lg"> 请在此页面不断完成随机电影评分，关于您的评分数据越多，评分效果越好哦！</p>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
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
                <div class="rating rating-md">
                  <input type="radio" :name="'rating-' + movie.movie_id" class="mask mask-star-2 bg-orange-400"
                         v-model="ratings[movie.movie_id]" :value="1" @change="updateRating(movie.movie_id, 1)"/>
                  <input type="radio" :name="'rating-' + movie.movie_id" class="mask mask-star-2 bg-orange-400"
                         v-model="ratings[movie.movie_id]" :value="2" @change="updateRating(movie.movie_id, 2)"/>
                  <input type="radio" :name="'rating-' + movie.movie_id" class="mask mask-star-2 bg-orange-400"
                         v-model="ratings[movie.movie_id]" :value="3" @change="updateRating(movie.movie_id, 3)"/>
                  <input type="radio" :name="'rating-' + movie.movie_id" class="mask mask-star-2 bg-orange-400"
                         v-model="ratings[movie.movie_id]" :value="4" @change="updateRating(movie.movie_id, 4)"/>
                  <input type="radio" :name="'rating-' + movie.movie_id" class="mask mask-star-2 bg-orange-400"
                         v-model="ratings[movie.movie_id]" :value="5" @change="updateRating(movie.movie_id, 5)"/>
                </div>
                <div class="flex items-center">
                  <button class="btn btn-circle btn-sm mr-2" @click="goToDetails(movie.movie_id)"> ></button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.text-primary {
  color: #00bcd4;
}

.btn-circle {
  margin-left: 10px;
}

.card:hover {
  transform: translateY(-4px);
}
</style>
