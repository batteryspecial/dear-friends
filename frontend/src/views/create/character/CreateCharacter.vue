<script setup lang="ts">
import { ref, useTemplateRef } from 'vue';
import Background from './_components/Background.vue';
import Description from './_components/Description.vue';
import Image from './_components/Image.vue';
import Name from './_components/Name.vue';
import { base64ToFile } from '@/js/utils/base64_to_file.ts';
import api from '@/js/http/api.ts';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user.ts';
import { isAxiosError } from 'axios';

// 6/13/2025 (Saturday)
// -> I decided to start using semicolons again

const router = useRouter()
const user = useUserStore()

const imageRef = useTemplateRef('image-ref');
const nameRef = useTemplateRef('name-ref');
const descRef = useTemplateRef('desc-ref');
const bgRef = useTemplateRef('bg-ref');

const errMsg = ref<string | null>(null);

async function handleCreate() {
    const image = imageRef.value?.newImage;
    const name = nameRef.value?.newName?.trim();
    const desc = descRef.value?.newDesc?.trim();
    const bg = bgRef.value?.newBackground;

    errMsg.value = '';

    if (!image) {
        errMsg.value = '头像不能为空';
    } else if (!name) {
        errMsg.value = '名字不能为空';
    } else if (!desc) {
        errMsg.value = '角色简介不能为空';
    } else {
        const formData = new FormData()
        formData.append('name', name);
        formData.append('desc', desc);
        formData.append('image', base64ToFile(image, 'image.png'));
        if (bg) formData.append('bg_image', base64ToFile(bg, 'background.png'));

        try {
            const r = await api.post('/api/create/character/create/', formData);
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
    <div class="flex justify-center">
        <div class="card w-120 bg-base200 shadow-md mt-[16vh]">
            <div class="card-body">
                <h3 class="card-title font-semibold!">创建角色</h3>
                <Image ref="image-ref" />
                <Name ref="name-ref"/>
                <Description ref="desc-ref"/>
                <Background ref="bg-ref"/>

                <p v-if="errMsg" class="text-red-500 text-sm">{{ errMsg }}</p>

                <div class="justify-end card-actions">
                    <button @click="handleCreate" class="btn btn-vue">创造</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>
