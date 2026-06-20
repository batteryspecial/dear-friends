<script setup lang="ts">
import api from '@/js/http/api';

import { ref, useTemplateRef, nextTick, onMounted, onBeforeUnmount } from 'vue';

import type { Character } from '../create/CreateIndex.vue';
import CharacterCard from '@/components/character/CharacterCard.vue';

type AllCharactersResponse = {
  result: 'success' | string;
  characters: Character[];
}

const characters = ref<Character[]>([]);

const isLoading = ref<boolean>(false);
const hasCharacters = ref<boolean>(true);

const sentinelRef = useTemplateRef<Element>("sentinel-ref")

function sentinelVisible(): boolean {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

async function loadMore(): Promise<void> {
    if (isLoading.value || !hasCharacters.value) return;
    isLoading.value = true;

    let newCharacters: Character[] = [];
    try {
        const r = await api.get("/api/homepage/index/", { params: { items_count: characters.value.length }});

        const data: AllCharactersResponse = r.data;
        if (data.result === "success") {
            newCharacters = data.characters;
        }
    } catch (err) {
        console.log(err)
    } finally {
        isLoading.value = false;
        if (newCharacters.length === 0) {
            hasCharacters.value = false;
        } else {
            characters.value.push(...newCharacters);
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

async function removeCharacter(characterId: number): Promise<void> {
    characters.value = characters.value.filter(c => c.id !== characterId)
}

onBeforeUnmount(() => {
    observer.disconnect();
})
</script>

<template>
    <div class="flex flex-col items-center mb-10">
        <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">
            <CharacterCard
                v-for="c in characters"
                :key="c.id"
                :character="c"
                :canEdit="false"
                @remove="removeCharacter"
            />
        </div>
        <div ref="sentinel-ref" class="h-2 w-100"></div>
        <div v-if="isLoading" class="text-slate-500 mt-5">加载中.&nbsp;&nbsp;.&nbsp;&nbsp;.&nbsp;&nbsp;.</div>
        <div v-else-if="!hasCharacters" class="text-slate-500 mt-5">_______________</div>
    </div>
</template>

<style scoped>

</style>
