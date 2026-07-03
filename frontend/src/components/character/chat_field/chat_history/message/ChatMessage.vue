<script setup lang="ts">
import { type Character } from '@/views/create/CreateIndex.vue';
import { type Message } from '../../ChatField.vue';
import { useUserStore } from '@/stores/user.ts';
import { computed } from 'vue';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

const { message, character } = defineProps(['message', 'character']) as {
    message: Message;
    character: Character;
}
const user = useUserStore();
const renderedContent = computed(() => DOMPurify.sanitize(marked.parse(message.content, { async: false })));
const messageTime = computed(() => new Date(message.createdAt).toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: 'numeric',
    hour12: true
}));
</script>

<template>
    <div v-if="message.role === 'ai'" class="chat chat-start text-white">
        <div class="chat-image avatar">
            <div class="w-10 rounded-full">
            <img
                alt="character image"
                :src="character.image"
            />
            </div>
        </div>
        <div class="chat-header">
            {{ character.name }}
            <time class="text-xs opacity-50">{{ messageTime }}</time>
        </div>
        <div class="chat-bubble prose prose-sm prose-invert max-w-none" v-html="renderedContent"></div>
        <div v-if="!message.pending" class="chat-footer opacity-50">Delivered</div>
    </div>
    <div v-else class="chat chat-end text-white">
        <div class="chat-image avatar">
            <div class="w-10 rounded-full">
            <img
                alt="user image"
                :src="user.image"
            />
            </div>
        </div>
        <div class="chat-header">
            {{ user.username }}
            <time class="text-xs opacity-50">{{ messageTime }}</time>
        </div>
        <div class="chat-bubble chat-bubble-success whitespace-pre-wrap">{{ message.content }}</div>
        <div class="chat-footer opacity-50">{{ messageTime }}</div>
    </div>
</template>

<style lang="css" scoped>

</style>
