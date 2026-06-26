<script setup lang="ts">
import type { Character } from '@/views/create/CreateIndex.vue';
const props = defineProps(["character"]) as { character: Character }
</script>

<template>
    <div class="absolute left-2 top-2 w-fit h-10 rounded-full bg-black/50 dark:bg-white/50 flex items-center gap-2 px-2 me-14">
        <div class="avatar">
            <div class="w-8 rounded-full">
                <img :src="props.character.image" alt="头像">
            </div>
        </div>
        <div class="text-black dark:text-white line-clamp-1 break-all">{{ character.name }}</div>
    </div>
</template>

<style scoped>

</style>
