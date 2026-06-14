<script setup lang="ts">
import { onMounted, ref, useTemplateRef } from 'vue';
import Background from './_components/Background.vue';
import Description from './_components/Description.vue';
import Image from './_components/Image.vue';
import Name from './_components/Name.vue';
import { base64ToFile } from '@/js/utils/base64_to_file.ts';
import api from '@/js/http/api.ts';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user.ts';
import { isAxiosError } from 'axios';

interface Character {
    id: string;
    name: string;
    desc: string;
    image: string;
    bg_image: string;
}

const route = useRoute();
const router = useRouter();
const user = useUserStore();

const characterId = route.params.character_id as string;
const character = ref<Character | null>(null);

onMounted(async () => {
    try {
        const r = await api.get("/api/create/character/get_character/", {
            params: { character_id: characterId }
        });

        const data = r.data;
        if (data.result === "success") {
            character.value = data.character;
        }
    } catch (err) {
        console.log(err);
    }
})

const imageRef = useTemplateRef('image-ref');
const nameRef = useTemplateRef('name-ref');
const descRef = useTemplateRef('desc-ref');
const bgRef = useTemplateRef('bg-ref');

const errMsg = ref<string | null>(null);

async function handleUpdate() {
    const newImage = imageRef.value?.newImage;
    const newName = nameRef.value?.newName?.trim();
    const newDesc = descRef.value?.newDesc?.trim();
    const newBgImage = bgRef.value?.newBackground;

    errMsg.value = '';

    if (!newImage) {
        errMsg.value = '头像不能为空';
    } else if (!newName) {
        errMsg.value = '名字不能为空';
    } else if (!newDesc) {
        errMsg.value = '角色简介不能为空';
    } else if (!newBgImage) {
        errMsg.value = '聊天背景不能为空';
    } else {
        const formData = new FormData();

        formData.append('character_id', characterId);
        formData.append('name', newName);
        formData.append('desc', newDesc);

        if (newImage !== character.value?.image)
            formData.append('image', base64ToFile(newImage, 'image.png'));
        if (newBgImage !== character.value?.bg_image)
            formData.append('bg_image', base64ToFile(newBgImage, 'background.png'));

        try {
            const r = await api.post('/api/create/character/update/', formData);
            const data = r.data;

            if (data.result === "success") {
                await router.push({
                    name: 'user_space',
                    params: { user_id: user.id },
                });
            } else {
                errMsg.value = data.result
            }
        } catch (err) {
            errMsg.value = (isAxiosError(err) ? err.response?.data?.result : null) ?? '请求失败，请稍后重试';
            console.log(err)
        }
    }
}
</script>

<template>
    <div v-if="character" class="flex justify-center">
        <div class="card w-120 bg-base200 shadow-md mt-[16vh]">
            <div class="card-body">
                <h3 class="card-title font-semibold!">更新角色</h3>
                <Image ref="image-ref" :image="character.image" />
                <Name ref="name-ref" :name="character.name"/>
                <Description ref="desc-ref" :desc="character.desc" />
                <Background ref="bg-ref" :bg="character.bg_image" />

                <p v-if="errMsg" class="text-red-500 text-sm">{{ errMsg }}</p>

                <div class="justify-end card-actions">
                    <button @click="handleUpdate" class="btn btn-vue">更新</button>
                </div>
            </div>
        </div>
    </div>
    <div v-else>Nothing...</div>
</template>

<style scoped>

</style>
