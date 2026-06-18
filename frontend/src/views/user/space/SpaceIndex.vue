<script setup lang="ts">    
import { onBeforeUnmount, onMounted, ref, useTemplateRef } from 'vue';
import { useRoute } from 'vue-router';
import UserInfoField from '../_components/UserInfoField.vue';
import CharacterCard from '@/components/character/CharacterCard.vue';
import api from '@/js/http/api.ts';
import { nextTick } from 'vue';
import { type Character } from '@/views/create/CreateIndex.vue';
import { type UserProfile } from '../_components/UserInfoField.vue';

type CharacterListResponse = {
  result: 'success' | string;
  user_profile: UserProfile;
  characters: Character[];
}

const userProfile = ref<UserProfile | null>(null);
const characters = ref<Character[]>([]);

const isLoading = ref<boolean>(false);
const hasCharacters = ref<boolean>(true);

const route = useRoute();
const sentinelRef = useTemplateRef<Element>("sentinel-ref")

function sentinelVisible(): boolean {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

async function loadMore(): Promise<void> {
    if (isLoading.value || !hasCharacters.value) return;
    isLoading.value = true;
    console.log("loading...")

    let newCharacters: Character[] = [];
    try {
        const r = await api.get("/api/create/character/get_many/", { params: {
            items_count: characters.value.length,
            user_id: route.params.user_id,
        }});

        const data: CharacterListResponse = r.data;
        if (data.result === "success") {
            userProfile.value = data.user_profile;
            newCharacters = data.characters;
        }
    } catch (err) {
        console.log(err)
    } finally {
        if (newCharacters.length === 0) {
            hasCharacters.value = false;
        } else {
            characters.value.push(...newCharacters);
            await nextTick(); // render, then determine
            if (sentinelRef.value && sentinelVisible()) await loadMore(); // real recursion!?
        }
        isLoading.value = false;
        console.log("loading complete")
    }
}

let observer: IntersectionObserver;
onMounted(async () => {
    await loadMore();

    observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) loadMore()
        })
    }, { root: null, rootMargin: '2px', threshold: 0 });

    observer.observe(sentinelRef.value as Element);
})

onBeforeUnmount(() => {
    observer.disconnect();
})
</script>

<template>
    <div class="flex flex-col items-center mb-10">
        <UserInfoField v-if="userProfile" :userProfile="userProfile"/>
        <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">
            <CharacterCard
                v-for="c in characters"
                :key="c.id"
                :character="c"
                :canEdit="true"
            />
        </div>
        <div ref="sentinel-ref" class="h-2 mt-8 w-100 bg-base-200"></div>
        <div v-if="isLoading" class="text-slate-500 mt-5">加载中.&nbsp;&nbsp;.&nbsp;&nbsp;.&nbsp;&nbsp;.</div>
        <div v-else-if="!hasCharacters" class="text-slate-500 mt-5">_______________</div>
    </div>
</template>

<style scoped>

</style>
