<script >
export default {
  methods: {
    goto_popular: function () {
      this.$router.push('/popular_movies')
    }
  }
}
</script>

<template>
  <div class="hero min-h-screen"
       style="background-image: url(https://img.daisyui.com/images/stock/photo-1507358522600-9f71e620c44e.jpg);">
    <div class="hero-overlay bg-opacity-60"></div>
    <div class="hero-content text-center text-neutral-content">
      <div class="max-w-md">
        <h1 class="mb-5 text-5xl font-bold">Hello there</h1>
        <p class="mb-5">Welcome to Movie Recommend System.</p>
        <button class="btn btn-primary" @click="goto_popular">Get Started</button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">

</style>