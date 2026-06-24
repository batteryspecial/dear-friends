<script setup lang="ts">
import { onMounted, ref, useTemplateRef } from 'vue';
import { FastAverageColor } from "fast-average-color"
import type { Character, Friend } from '@/views/create/CreateIndex.vue';
import { useUserStore } from '@/stores/user';
import { RouterLink, useRouter } from 'vue-router';
import UpdateIcon from '../icons/update.vue';
import RemoveIcon from '../icons/remove.vue';
import api from '@/js/http/api.ts';
import ChatField from './chat_field/ChatField.vue';

const { character, canEdit } = defineProps(['character', 'canEdit']) as { 
    character: Character;
    canEdit: boolean;
};
const emit = defineEmits(["remove"]);
const isHover = ref<boolean>(false);
const user = useUserStore();
const router = useRouter();
const avgColorRef = ref<string>('');
const chatFieldRef = useTemplateRef("chat-field-ref");
const friend = ref<Friend | null>(null)

async function openChatField() {
    if (!user.isLoggedIn()) await router.push({ name: 'user_login' })
    else {
        try {
            const r = await api.post("/api/friend/get_create/", {
                character_id: character.id
            })
            if (r.data.result === "success") {
                friend.value = r.data.friend;
                chatFieldRef.value?.showModal()
            }
        } catch (err) {
            console.log(err)
        }
    }
}

const fac = new FastAverageColor();

async function handleRemoveCharacter() {
    const isConfirmed = window.confirm("你确定要删除这个角色吗？\n数据会被永久消除。");
    if (!isConfirmed) return

    try {
        const r = await api.post("/api/create/character/delete/", {
            character_id: character.id,
        });
        if (r.data.result === "success") {
            emit("remove", character.id);
        } else {
            console.log(r.data.result)
        }
    } catch (err) {
        console.log(err)
    }
}

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
        <div class="avatar cursor-pointer" @mouseover="isHover=true" @mouseout="isHover=false" @click="openChatField">
            <div class="w-60 h-100 rounded-2xl relative">
                <img :src="character.bg_image" class="transition-all duration-300" :class="{'brightness-75 scale-105' : isHover}" alt="image" draggable="false">
                <div class="absolute left-0 top-50 w-60 h-50 bg-linear-to-t from-black/40 to-transparent"></div>

                <div 
                    v-if="canEdit && user.id === character.author.user_id"
                    class="absolute right-2 top-1 transition-all duration-500"
                    :class="isHover ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-50'"
                >
                    <RouterLink 
                        :to="{name: 'update_character', params: { character_id: character.id }}"
                        class="btn btn-circle btn-ghost"
                    >
                        <UpdateIcon />
                    </RouterLink>
                    <button @click="handleRemoveCharacter" class="btn btn-circle btn-ghost hover:bg-red-500/40">
                        <RemoveIcon />
                    </button>
                </div>

                <div class="absolute left-5 bottom-5 flex flex-col items-start gap-2">
                    <div class="avatar">
                        <div 
                            class="w-16 rounded-full shadow-lg ring-3 transition-colors duration-300"
                            :style="{'--tw-ring-color' : avgColorRef || '#3b82f6'}"
                        >
                            <img :src="character.image" alt="character profile image" draggable="false" class="select-none">
                        </div>
                    </div>
                    <div 
                        class="grid transition-all duration-500 ease-out"
                        :class="isHover ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0'"
                    >
                        <div class="overflow-hidden">
                            <div class="text-white text-lg font-bold">{{ character.name }}</div>
                            <p class="text-white mt-1">
                                {{ character.desc }}
                            </p>
                        </div>
                    </div>
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
        <ChatField ref="chat-field-ref" :friend="friend" />
    </div>
</template>

<style scoped>

</style>
