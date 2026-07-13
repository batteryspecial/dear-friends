<script setup lang="ts">
import type { Friend } from '@/views/create/CreateIndex.vue';
import { useTemplateRef, computed, ref, nextTick } from 'vue';
import InputField from './input_field/InputField.vue';
import CharacterImageField from './image_field/CharacterImageField.vue';
import ChatHistory from './chat_history/ChatHistory.vue';

export interface Message {
    id: string;
    role: string;
    content: string;
    pending: boolean;
    createdAt: string;
}

const { friend, color } = defineProps(["friend", "color"]) as {
    friend: Friend,
    color: string
}
const modalRef = useTemplateRef("modal-ref")
const inputFieldRef = useTemplateRef("input-field-ref")
const chatHistoryRef = useTemplateRef("chat-history-ref");
const opened = ref(false);
const history = ref<Message[]>([]);

async function showModal() {
    modalRef.value?.showModal();
    await nextTick();
    inputFieldRef.value?.focusChatInput();
    requestAnimationFrame(() => { opened.value = true })
}

function handlePushMessage(msg: Message): void {
    history.value.push(msg);
    chatHistoryRef.value?.followOutput();
}
function handlePushFrontMessage(msg: Message): void {
    history.value.unshift(msg);
}

function handleAppendLastMessage(delta: string): void {
    const last_message = history.value.at(-1);
    if (last_message) last_message.content += delta;
    chatHistoryRef.value?.followOutput();
}

function handleCompleteLastMessage(): void {
    const last_message = history.value.at(-1);
    if (last_message) last_message.pending = false;
}

function handleClose() {
    modalRef.value?.close();
    inputFieldRef.value?.close();
}

const bgStyle = computed(() => {
    return friend ? { backgroundImage: `linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.25)), url(${friend.character.bg_image})` } : {}
})

defineExpose({
    showModal,
})
</script>

<template>
    <dialog ref="modal-ref" class="modal" @close="opened = false">
        <div class="modal-box w-90 h-150 overflow-hidden">
            <div
                class="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat transition-all duration-500 ease-out"
                :class="opened ? 'blur-xs scale-105' : 'blur-none scale-100'"
                :style="bgStyle"
            ></div>
            <form @submit="handleClose" method="dialog" class="absolute top-0 right-0 z-10">
                <button class="btn btn-md btn-circle btn-ghost absolute right-2 top-2">✕</button>
            </form>
            <ChatHistory
                ref="chat-history-ref"
                v-if="friend"
                :history="history"
                :friendId="friend.id"
                :character="friend.character"
                @pushFrontMessage="handlePushFrontMessage"
            />
            <InputField
                v-if="friend" 
                :color="color" 
                :friendId="friend.id" 
                ref="input-field-ref" 
                @pushMessage="handlePushMessage"
                @appendLastMessage="handleAppendLastMessage"
                @completeLastMessage="handleCompleteLastMessage"
            />
            <CharacterImageField
                v-if="friend" 
                :character="friend.character"
            />
        </div>
    </dialog>
</template>

<style scoped>

</style>
