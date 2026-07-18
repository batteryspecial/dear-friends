<script setup lang="ts">
import MicIcon from '@/components/icons/mic.vue';
import SendIcon from '@/components/icons/send.vue';
import stream from '@/js/http/streaming';
import { onUnmounted, ref, useTemplateRef } from 'vue';
import Microphone from './Microphone.vue';
import { teardownAudio, stopAudio, handleAudioChunk, initAudioStream } from '@/js/utils/audio.ts';

const { color, friendId } = defineProps(["color", "friendId"]) as {
    color: string,
    friendId: number,
}
const emit = defineEmits(['pushMessage', 'appendLastMessage', 'completeLastMessage'])
const chatInputRef = useTemplateRef("chat-input-ref")
const processId = ref<number>(0);
const showMic = ref<boolean>(false);
const message = ref<string>('');

onUnmounted(() => {
    teardownAudio();
});

function handleStop() { processId.value++; stopAudio(); }
function focusChatInput() { chatInputRef.value?.focus(); }
function close() { processId.value++; showMic.value = false; stopAudio(); }

async function handleSend(event: Event, audio_msg?: string): Promise<void> {
    let content: string | null = null;
    if (audio_msg) {
        content = audio_msg.trim()
    } else {
        content = message.value.trim()
    }
    if (!content) return;

    initAudioStream(); // 初始化一个音频播放器 
    
    message.value = "";
    const currentId = ++processId.value;

    const now = new Date().toISOString();
    emit("pushMessage", { role: "user", content: content, id: crypto.randomUUID(), pending: false, createdAt: now });
    emit("pushMessage", { role: "ai", content: '', id: crypto.randomUUID(), pending: true, createdAt: now });

    try {
        await stream('/api/friend/message/chat/', {
            body: {
                friend_id: friendId,
                message: content
            },
            onmessage(data, isDone) {
                if (currentId !== processId.value) return
                if (isDone) {
                    emit("completeLastMessage");
                }
                if (typeof data !== "object") return    
                if (data.content) {
                    emit("appendLastMessage", data.content);
                }
                if (data.audio) {
                    handleAudioChunk(data.audio);
                }
            },
            onerror(err) {
                console.log(err)
            }
        })
    } catch (err) {
        console.log(err)
    }
}

defineExpose({
    focusChatInput,
    close
})
</script>

<template>
    <form v-if="!showMic" @submit.prevent="handleSend" class="absolute bottom-4 left-2 h-12 w-86 flex items-center">
        <input
            ref="chat-input-ref"
            v-model="message"
            class="input w-full pr-17 whitespace-pre-wrap break-words rounded-2xl bg-black/30 backdrop-blur-sm border !border-[color:var(--avg-color)] text-white text-base"
            :style="{ '--avg-color': color }"
            type="text"
            placeholder="文本输入..."
        >
        <div class="absolute right-10 w-8 h-8 flex justify-center items-center cursor-pointer">
            <SendIcon @click="handleSend" class="stroke-white hover:stroke-[color-mix(in_srgb,var(--avg-color)_50%,white)] transition-colors duration-300" :style="{ '--avg-color': color }" />
        </div>
        <div @click="showMic = true" class="absolute right-2 w-8 h-8 flex justify-center items-center cursor-pointer">
            <MicIcon class="stroke-white hover:stroke-[color-mix(in_srgb,var(--avg-color)_50%,white)] transition-colors duration-300" :style="{ '--avg-color': color }" />
        </div>
        
    </form>
    <Microphone 
        v-else 
        @close="showMic = false" 
        @send="handleSend"
        @stop="handleStop"
        :color="color" 
    />
</template>

<style scoped>

</style>
