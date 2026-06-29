<script setup lang="ts">
import MicIcon from '@/components/icons/mic.vue';
import SendIcon from '@/components/icons/send.vue';
import api from '@/js/http/api'; 
import stream from '@/js/http/streaming';
import { ref, useTemplateRef } from 'vue';

const { color, friendId } = defineProps(["color", "friendId"]) as {
    color: string,
    friendId: number,
}
const message = ref<string>('')
const isProcessing = ref<boolean>(false)
const chatInputRef = useTemplateRef("chat-input-ref")

function focusChatInput() {
    chatInputRef.value?.focus();
}

async function handleSend(): Promise<void> {
    const content = message.value.trim()
    if (!content) return;
    message.value = "";

    try {
        await stream('/api/friend/message/chat/', {
            body: {
                friend_id: friendId,
                message: content
            },
            onmessage(data, isDone) {
                if (isDone) isProcessing.value = false
                else if (typeof data === "object" && data) console.log(data.content)
            },
            onerror(err) {
                console.log(err)
                isProcessing.value = false
            }
        })
    } catch (err) {
        console.log(err)
        isProcessing.value = false
    }
}

defineExpose({
    focusChatInput,
})
</script>

<template>
    <form @submit.prevent="handleSend" class="absolute bottom-4 left-2 h-12 w-86 flex items-center">
        <input
            ref="chat-input-ref"
            v-model="message"
            class="input w-full pr-17 rounded-2xl bg-black/30 backdrop-blur-sm border !border-[color:var(--avg-color)] text-white text-base"
            :style="{ '--avg-color': color }"
            type="text"
            placeholder="文本输入..."
        >
        <div class="absolute right-2 w-8 h-8 flex justify-center items-center cursor-pointer">
            <SendIcon @click="handleSend" class="stroke-white hover:stroke-[color-mix(in_srgb,var(--avg-color)_50%,white)] transition-colors duration-300" :style="{ '--avg-color': color }" />
        </div>
        <div class="absolute right-9 w-8 h-8 flex justify-center items-center cursor-pointer">
            <MicIcon class="stroke-white hover:stroke-[color-mix(in_srgb,var(--avg-color)_50%,white)] transition-colors duration-300" :style="{ '--avg-color': color }" />
        </div>
    </form>
</template>

<style scoped>

</style>
