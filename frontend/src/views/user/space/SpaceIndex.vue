<script setup>
import { useRoute, useRouter } from 'vue-router';

const route = useRoute()
const router = useRouter()

router.push({
    name: 'user_space'
})
</script>

<template>
    <div>
        个人空间 
        <span class="text-bold">{{ route.params.user_id }}</span>
    </div>
</template>

<style scoped>

</style>
