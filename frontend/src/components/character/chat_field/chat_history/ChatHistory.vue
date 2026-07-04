<script setup lang="ts">
import { type Character } from '@/views/create/CreateIndex.vue';
import { type Message } from '../ChatField.vue';
import ChatMessage from './message/ChatMessage.vue';
import { nextTick, onBeforeUnmount, onMounted, useTemplateRef } from 'vue';
import api from '@/js/http/api.ts';

type MessageHistoryResponse = {
    id: number;
    user_message: string;
    output: string;
    created_at: string;
}

const { history, friendId, character } = defineProps(['history', 'friendId', 'character']) as {
    history: Message[];
    friendId: number;
    character: Character;
}
const emits = defineEmits(['pushFrontMessage'])
const scrollRef = useTemplateRef("scroll-ref");
const sentinelRef = useTemplateRef("sentinel-ref");
async function followOutput(): Promise<void> {
    await nextTick();
    const viewport = scrollRef.value;
    if (viewport) viewport.scrollTop = viewport.scrollHeight;
}


let isLoading: boolean = false;
let moreMessages: boolean = true;
let lastMessageId: number = 0;

function sentinelVisible() {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const sentinelRect = sentinelRef.value.getBoundingClientRect()
  const scrollRect = (scrollRef.value ?? new HTMLDivElement).getBoundingClientRect()
  return sentinelRect.top < scrollRect.bottom && sentinelRect.bottom > scrollRect.top
}

async function loadMore(): Promise<void> {
    if (isLoading || !moreMessages) return;
    isLoading = true;

    let oldMessages: MessageHistoryResponse[] = []
    try {
        const r = await api.get('/api/friend/message/get_history/', {
            params: {
                last_message_id: lastMessageId,
                friend_id: friendId
            }
        })
        const data = r.data;
        if (data.result === "success") {
            oldMessages = data.messages;
        }
    } catch (err) {
        console.log(err)
    } finally {
        isLoading = false;

        if (oldMessages.length === 0) {
            moreMessages = false;
        } else {
            const viewport = scrollRef.value;
            const oldHeight = viewport?.scrollHeight ?? 0;
            const oldTop = viewport?.scrollTop ?? 0;

            for (const msg of oldMessages) {
                emits("pushFrontMessage", {
                    id: crypto.randomUUID(),
                    role: 'ai',
                    content: msg.output,
                    pending: false,
                    createdAt: msg.created_at,
                });
                emits("pushFrontMessage", {
                    id: crypto.randomUUID(),
                    role: 'user',
                    content: msg.user_message,
                    pending: false,
                    createdAt: msg.created_at,
                });
                lastMessageId = msg.id;
            }
            await nextTick();
            // keep the same content on screen after prepending older messages
            if (viewport) viewport.scrollTop = oldTop + viewport.scrollHeight - oldHeight;
            if (sentinelVisible()) await loadMore();
        }
    }
}

let observer: IntersectionObserver;
onMounted(async () => {
    await loadMore();
    await followOutput();

    observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) loadMore();
        })
    }, { root: scrollRef.value, rootMargin: '2px', threshold: 0 });

    observer.observe(sentinelRef.value as Element);
})

onBeforeUnmount(() => {
    observer?.disconnect();
})

defineExpose({
    followOutput,
})
</script>

<template>
    <div ref="scroll-ref" class="absolute top-14 left-0 w-90 h-120 overflow-y-scroll">
        <!-- sentinel must NOT be display:none (`hidden`) — IntersectionObserver
             never fires on display:none elements. Transparent is invisible enough. -->
        <div ref="sentinel-ref" class="h-2"></div>
        <ChatMessage
            v-for="m in history"
            :key="m.id"
            :message="m"
            :character="character"
            class="flex-1 min-h-0"
        />
    </div>
</template>

<style lang="css" scoped>

</style>
