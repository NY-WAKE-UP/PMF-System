<template>
  <div class="hero min-h-screen"
       style="background-image: url(https://img.daisyui.com/images/stock/photo-1507358522600-9f71e620c44e.jpg);">
    <div class="hero-overlay bg-opacity-50"></div>
    <div class="hero max-w-md ">
      <div class="hero-content flex-col lg:flex-row-reverse">
        <div class="card shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
          <form class="card-body" @submit.prevent="registerUser">
            <div class="form-control">
              <label class="label">
                <span class="label-text">Username</span>
              </label>
              <input type="text" placeholder="Username" class="input input-bordered" v-model="username" required />
            </div>
            <div class="form-control">
              <label class="label">
                <span class="label-text">Email</span>
              </label>
              <input type="email" placeholder="Email" class="input input-bordered" v-model="email" required />
            </div>
            <div class="form-control">
              <label class="label">
                <span class="label-text">Password</span>
              </label>
              <input type="password" placeholder="Password" class="input input-bordered" v-model="password" required />
            </div>
            <div class="form-control mt-6">
              <button type="submit" class="btn btn-primary">SignUp</button>
            </div>
            <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
          </form>
        </div>
        <div class="text-center lg:text-left">
          <h1 class="text-5xl font-bold text-cyan-600">Signup</h1>
          <p class="py-6 text-white">Movie Recommend System</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    async registerUser() {
      try {
        const response = await fetch('http://localhost:8000/signup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password
          })
        });
        const data = await response.json();
        if (!response.ok) {
          this.errorMessage = data.detail;
        } else {
          this.errorMessage = '';
          alert("Registration successful!");
          this.$router.push('/login'); // Redirect to login page after successful registration
        }
      } catch (error) {
        console.error("Registration failed:", error);
        this.errorMessage = "Registration failed. Please try again.";
      }
    }
  }
}
</script>

<style scoped lang="scss">

</style>
