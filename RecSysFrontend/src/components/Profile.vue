<template>
  <div>
    <SiteNavigation/>
    <Menu/>
    <div class="hero min-h-screen bg-cover bg-center"
         style="background-image: url(https://img.daisyui.com/images/stock/photo-1507358522600-9f71e620c44e.jpg);">
      <div class="hero-overlay bg-black bg-opacity-50"></div>
      <div class="container mx-auto py-12">
        <h1 class="text-3xl font-semibold text-white mb-6">个人信息</h1>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h2 class="text-xl font-semibold text-white mb-4">修改头像</h2>
            <div class="flex items-center">
              <input ref="fileInput" type="file" @change="handleFileChange" class="input input-bordered w-full mr-2">
            </div>
            <div v-if="avatarUrl" class="mt-4">
              <img :src="avatarUrl" alt="avatar" class="w-32 h-32 rounded-full">
            </div>
          </div>
          <div>
            <h2 class="text-xl font-semibold text-white mb-4">修改邮箱</h2>
            <input v-model="email" type="email" placeholder="新邮箱" class="input input-bordered w-full mb-2">
          </div>
          <div>
            <h2 class="text-xl font-semibold text-white mb-4">修改密码</h2>
            <input v-model="password" type="password" placeholder="新密码" class="input input-bordered w-full mb-2">
            <input v-model="confirmPassword" type="password" placeholder="确认新密码" class="input input-bordered w-full mb-2">
            <p v-if="passwordMismatch" class="text-red-500">密码不匹配，请重新输入。</p>
          </div>
        </div>
        <div class="mt-6">
          <button @click="saveChanges" class="btn btn-primary">保存</button>
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
  name: "UserProfile",
  components: {Menu, SiteNavigation},
  data() {
    return {
      avatarUrl: '', // 用户输入的头像链接
      email: '', // 用户输入的邮箱
      password: '', // 用户输入的密码
      confirmPassword: '', // 用户输入的确认密码
      file: null, // 用户上传的文件
      userId: sessionStorage.getItem('user_id'), // 当前用户的ID
      username: sessionStorage.getItem('username'),
      passwordMismatch: false // 密码不匹配的标志
    }
  },
  created() {
    axios.get(`http://localhost:8000/account/${this.username}`)
        .then(response => {
          const userData = response.data;
          this.avatarUrl = userData.avatar;
          this.email = userData.email;
        })
        .catch(error => {
          console.error('Error fetching user data:', error);
        });
  },
  methods: {
    handleFileChange(event) {
      this.file = event.target.files[0];
      this.avatarUrl = URL.createObjectURL(this.file);
    },
    async saveChanges() {
      // 验证密码和确认密码是否匹配
      if (this.password !== this.confirmPassword) {
        this.passwordMismatch = true;
        return;
      }

      this.passwordMismatch = false;
      const formData = new FormData();
      formData.append('id', this.userId);
      formData.append('username', this.username);
      formData.append('email', this.email);
      formData.append('password', this.password);
      if (this.file) {
        formData.append('file', this.file);
      }

      try {
        const response = await axios.put(`http://localhost:8000/account/update`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('User profile updated successfully:', response.data);
        alert('个人信息已保存！');
      } catch (error) {
        console.error('Error updating user profile:', error);
        alert('个人信息保存失败！');
      }
    }
  }
}
</script>

<style scoped lang="scss">
.hero {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-position: center;
  background-size: cover;
}
.hero-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}
.container {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
}
.input {
  background-color: rgba(255, 255, 255, 0.8);
}
.btn-primary {
  background-color: #21ac7c;
  border-color: #21ac7c;
}
.btn-primary:hover {
  background-color: rgba(33, 172, 124, 0.73);
  border-color: rgba(33, 172, 124, 0.73);
}
.text-red-500 {
  color: #f56565;
}
</style>
