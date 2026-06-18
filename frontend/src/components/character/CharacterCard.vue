<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { FastAverageColor } from "fast-average-color"
import { type Character } from '@/views/create/CreateIndex.vue';
import { useUserStore } from '@/stores/user';
import { RouterLink } from 'vue-router';
import UpdateIcon from '../icons/update.vue';
import RemoveIcon from '../icons/remove.vue';

const { character, canEdit } = defineProps(['character', 'canEdit']) as { 
    character: Character;
    canEdit: boolean;
}
const isHover = ref<boolean>(false)
const user = useUserStore()
const avgColorRef = ref<string>('')

const fac = new FastAverageColor();

onMounted(async () => {
    if (character.image) {
        fac.getColorAsync(character.image, { crossOrigin: "anonymous" })
        .then(color => {
            avgColorRef.value = color.hex;
        })
        .catch(err => {
            console.error("Failed to get average color:", err);
            avgColorRef.value = '#3b82f6'; // fallback color (e.g. Tailwind blue-500) if image fails
        });
    }
})
</script>

<template>
    <div>
        <div class="avatar cursor-pointer" @mouseover="isHover=true" @mouseout="isHover=false">
            <div class="w-60 h-100 rounded-2xl relative">
                <img :src="character.bg_image" class="transition-all duration-300" :class="{'brightness-75 scale-105' : isHover}" alt="image">
                <div class="absolute left-0 top-50 w-60 h-50 bg-linear-to-t from-black/40 to-transparent"></div>

                <div 
                    v-if="canEdit && user.id === character.author.user_id"
                    class="absolute right-0 top-0"
                >
                    <RouterLink 
                        :to="{name: 'update_character', params: { character_id: character.id }}"
                        class="btn btn-circle btn-ghost"
                    >
                        <UpdateIcon />
                    </RouterLink>
                    <button class="btn btn-circle btn-ghost hover:bg-red-500/40">
                        <RemoveIcon />
                    </button>
                </div>

                <div 
                    class="absolute left-5 bottom-0 flex flex-col items-start gap-2 transition-all duration-500 ease-out"
                    :class="{'translate-y-0 opacity-100 pointer-events-auto' : isHover, 'translate-y-full opacity-50 pointer-events-none' : !isHover}"
                >
                    <div class="avatar">
                        <div 
                            class="w-16 rounded-full shadow-lg ring-3 transition-colors duration-300"
                            :style="{'--tw-ring-color' : avgColorRef || '#3b82f6'}"
                        >
                            <img :src="character.image" alt="character profile image">
                        </div>
                    </div>
                    <div class="text-white text-lg! font-bold!">{{ character.name }}</div>
                    <p class="text-white mb-5">
                        {{ character.desc }}
                    </p>
                </div>
            </div>
        </div>
        <RouterLink :to="{name: 'user_space', params: { user_id: character.author.user_id }}" class="flex items-center mt-2 p-2 gap-2 rounded-xl">
            <div class="avatar">
                <div class="w-7 rounded-full">
                    <img :src="character.author.image" alt="author profile image">
                </div>
            </div>
            <div class="text-sm! line-clamp-1 break-all">
                {{ character.author.username }}
            </div>
        </RouterLink>
    </div>
</template>

<style scoped>

</style>
