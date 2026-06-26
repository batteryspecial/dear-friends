<script setup lang="ts">
import api from '@/js/http/api';

import { ref, watch, useTemplateRef, nextTick, onMounted, onBeforeUnmount } from 'vue';
import { useRoute } from 'vue-router';

import type { Friend } from '../create/CreateIndex.vue';
import CharacterCard from '@/components/character/CharacterCard.vue';

type AllCharactersResponse = {
  result: 'success' | string;
  friends: Friend[];
}

const route = useRoute();

const friends = ref<Friend[]>([]);
const isLoading = ref<boolean>(false);
const hasMoreFriends = ref<boolean>(true);

const sentinelRef = useTemplateRef<Element>("sentinel-ref")

function sentinelVisible(): boolean {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

async function loadMore(): Promise<void> {
    if (isLoading.value || !hasMoreFriends.value) return;
    isLoading.value = true;

    let newFriends: Friend[] = [];
    try {
        const r = await api.get("/api/friend/get_list/", { 
            params: { 
                items_count: friends.value.length,
                search_query: (typeof route.query.q === "string" ? route.query.q : ''),
            }
        });

        const data: AllCharactersResponse = r.data;
        if (data.result === "success") {
            newFriends = data.friends;
        }
    } catch (err) {
        console.log(err)
    } finally {
        isLoading.value = false;
        if (newFriends.length === 0) {
            hasMoreFriends.value = false;
        } else {
            friends.value.push(...newFriends);
            await nextTick(); // render, then determine
            if (sentinelRef.value && sentinelVisible()) await loadMore(); // real recursion!?
        }
    }
}

let observer: IntersectionObserver;
onMounted(async () => {
    await loadMore();
    observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) loadMore();
        })
    }, { root: null, rootMargin: '2px', threshold: 0 });

    observer.observe(sentinelRef.value as Element);
})

async function removeFriend(friendId: number): Promise<void> {
    friends.value = friends.value.filter(f => f.id !== friendId)
}


onBeforeUnmount(() => {
    observer.disconnect();
})
</script>

<template>
    <div class="flex flex-col items-center mb-10">
        <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">
            <CharacterCard
                v-for="f in friends"
                :key="f.id"
                :character="f.character"
                :canRemoveFriend="true"
                :friend="f"
                @remove="removeFriend"
            />
        </div>
        <div ref="sentinel-ref" class="h-2 w-100"></div>
        <div v-if="isLoading" class="text-slate-500 mt-5">加载中.&nbsp;&nbsp;.&nbsp;&nbsp;.&nbsp;&nbsp;.</div>
        <div v-else-if="!hasMoreFriends" class="text-slate-500 mt-5">_______________</div>
    </div>
</template>

<style scoped>

</style>
