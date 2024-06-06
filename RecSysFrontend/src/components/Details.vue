<template>
  <div>
    <SiteNavigation />
    <Menu />
    <div
        class="hero min-h-screen"
        :style="{ 'background-image': `url(${backgroundImage})` }"
    >
      <div class="hero-overlay bg-opacity-50"></div>
      <div class="hero-content w-1/2 h-1/2 lg:flex-row" v-if="movie">
        <img :src="movie.image_url" class="max-w-sm rounded-lg shadow-2xl" />
        <div class="flex-col">
          <h1 class="text-5xl font-bold text-white">{{ movie.movie_title }}</h1>

          <p class="py-6 text-white">{{ additionalContent }}</p>
          <div class=" ">
            <button class="btn btn-xs w-fit justify-start">
              rating
              <div class="badge badge-secondary badge-sm">{{ movie.movie_rating }}</div>
            </button>
            <span @click="goToGenre(movie.genre)"
                  class="btn btn-xs">{{ movie.genre }}</span>
          </div>
        </div>

        <div class="rating rating-md">
          <input type="radio" name="rating-7" class="mask mask-star-2 bg-orange-400" v-model="rating" :value="1" />
          <input type="radio" name="rating-7" class="mask mask-star-2 bg-orange-400" v-model="rating" :value="2" />
          <input type="radio" name="rating-7" class="mask mask-star-2 bg-orange-400" v-model="rating" :value="3" />
          <input type="radio" name="rating-7" class="mask mask-star-2 bg-orange-400" v-model="rating" :value="4" />
          <input type="radio" name="rating-7" class="mask mask-star-2 bg-orange-400" v-model="rating" :value="5" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useRoute } from "vue-router";
import SiteNavigation from "@/components/SiteNavigation.vue";
import Menu from "@/components/Menu.vue";

export default {
  components: {
    SiteNavigation,
    Menu,
  },
  data() {
    return {
      movieId: this.$route.params.movieId,
      movie: null,
      additionalContent: null,
      rating: null,
      username: sessionStorage.getItem("username"),
    };
  },
  async mounted() {
    try {
      // 获取电影详情
      const response = await axios.get(`http://localhost:8000/movies/details/${this.movieId}`);
      this.movie = response.data;
      // 设置初始评分为电影的评分
      if (this.movie && this.movie.movie_rating) {
        this.rating = this.movie.movie_rating;
      }else console.log("nonon")
      // 获取额外内容
      if (this.movie && this.movie.movie_title) {
        const additionalResponse = await axios.get(`http://localhost:8000/movies/content/${this.movie.movie_title}`);
        this.additionalContent = additionalResponse.data;
      }

      // 获取背景图片
      this.backgroundImage = "https://img.daisyui.com/images/stock/photo-1507358522600-9f71e620c44e.jpg";
    } catch (error) {
      console.error('Error fetching movie details:', error);
    }
  },
  watch: {
    rating(newRating) {
      if (newRating && this.movieId) {
        this.submitRating(newRating);
      }
    },
  },
  methods: {
    async submitRating(newRating) {
      try {
        const ratingResponse = await axios.post(`http://localhost:8000/movies/ratings`, {
          movie_id: this.movieId,
          username: this.username,
          rating: newRating,
        });
        console.log('Rating submitted successfully:', ratingResponse.data);
      } catch (error) {
        console.error('Error submitting rating:', error);
      }
    },
    goToGenre(genre) {
      this.$router.push({ name: 'genreMovies', params: { genre } });
    }
  },
};
</script>

<style scoped lang="scss">
</style>
