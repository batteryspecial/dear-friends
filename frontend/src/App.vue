<script setup lang="ts">
import HomeView from './views/HomeView.vue';
import { useRoute, useRouter } from 'vue-router';
import { onMounted } from 'vue';

import { useUserStore } from './stores/user';
import api from './js/http/api';


const user = useUserStore()
const router = useRouter()
const route = useRoute()

onMounted(async () => {
  try {
    const r = await api.get('/api/user/account/get_user_info/')
    const data = r.data

    if (data.result === 'success') {
      user.setUserInfo(data)
    }

  } catch (err) {
    console.log(err)
  } finally {
    user.setHasPulledUserInfo(true)

    if (route.meta.needLogin && !user.isLoggedIn()) {
      // no going back >=)
      await router.replace({
        name: 'homepage_index',
      })
    }
  }
})
</script>

<template>
  <HomeView />
</template>

<style scoped>

</style>
