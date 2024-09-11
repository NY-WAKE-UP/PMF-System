<script>
import axios from "axios";

export default {
  data() {
    return {
      username: '', // 添加 username 字段
      email:'',
      password:'',
      user_id:''
    }
  },
  methods: {
    goto_signup: function () {
      this.$router.push('/signup')
    },
    async confirm(event) {
      event.preventDefault(); // 阻止默认的表单提交行为
      try {
        const response = await axios.post('http://localhost:8000/signin', {
          username: this.username,
          email:this.email,
          password:this.password
        });
        const user=await axios.get(`http://localhost:8000/account/${this.username}`)
        this.user_id=user.data.id
        // const token = response.data.access_token;
        // sessionStorage.setItem('token', token); // 使用会话存储空间
        sessionStorage.setItem('username', this.username); // 使用会话存储空间
        sessionStorage.setItem('user_id',this.user_id)
        this.$router.push('/popular_movies')
      } catch (error) {
        console.error("Login failed:", error);
        alert("Login failed. Please check your credentials and try again.");
      }

    }
  }
}

</script>


<template>
  <div class="hero min-h-screen"
       style="background-image: url(https://img.daisyui.com/images/stock/photo-1507358522600-9f71e620c44e.webp);">
    <div class="hero-overlay bg-opacity-50"></div>
    <div class="hero max-w-md ">
      <div class="hero-content flex-col lg:flex-row-reverse">

        <div class="card shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
          <form class="card-body">
            <div class="form-control">
              <label class="label">
                <span class="label-text">name</span>
              </label>
              <input type="text" placeholder="username" class="input input-bordered" v-model="username" required/>
              <!-- 使用 v-model 绑定输入框 -->
            </div>
            <div class="form-control">
              <label class="label">
                <span class="label-text">Email</span>
              </label>
              <input type="email" placeholder="email" class="input input-bordered" v-model="email" required/>
            </div>
            <div class="form-control">
              <label class="label">
                <span class="label-text">Password</span>
              </label>
              <input type="password" placeholder="password" class="input input-bordered" v-model="password" required/>
              <!-- 使用 v-model 绑定输入框 -->
              <label class="label">
                <a href="#" class="label-text-alt link link-hover" @click="goto_signup">signup?</a>
              </label>
            </div>
            <div class="form-control mt-6">
              <button class="btn btn-primary" @click="confirm">Login</button> <!-- 将 @click 事件绑定到 confirm 方法 -->
            </div>
          </form>
        </div>
        <div class="text-center lg:text-left">
          <h1 class="text-5xl font-bold text-cyan-600">Login</h1>
          <p class="py-6 text-white"> Movie Recommend System</p>
        </div>
      </div>
    </div>
  </div>

</template>

<style scoped lang="scss">

</style>
