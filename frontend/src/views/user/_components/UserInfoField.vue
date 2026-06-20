<script setup lang="ts">
export interface UserProfile {
  user_id: number;
  username: string;
  bio: string;
  image: string;
}

const { userProfile: UserProfile } = defineProps(['userProfile'])
</script>

<template>
  <div class="bg-base-200 w-full">
    <div class="flex my-12 gap-8 justify-center">
      <div class="avatar">
        <div class="w-40 rounded-full">
          <img :src="userProfile.image" alt="profile image">
        </div>
      </div>
      <div class="flex flex-col justify-center w-65 h-40">
        <div class="text-2xl font-bold! line-clamp-1 break-all">{{ userProfile.username }}</div>
        <div class="text-slate-500 ">用户 #{{ userProfile.user_id }}</div>
        <p class="mt-5 h-20 line-clamp-5 break-all">{{ userProfile.bio }}</p>
      </div>
    </div>
  </div>
  
    
</template>

<style scoped>

</style>
