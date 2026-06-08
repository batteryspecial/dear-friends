<script setup lang="ts">
import Bio from './_components/Bio.vue';
import Image from './_components/Image.vue';
import Username from './_components/Username.vue';

import api from '@/js/http/api.ts';
import { type UserInfo } from '@/stores/user';
import { useTemplateRef, ref } from 'vue';
import { useUserStore } from '@/stores/user';
import { base64ToFile } from '@/js/utils/base64_to_file.ts';

const user = useUserStore()

const imageRef = useTemplateRef('image-ref')
const usernameRef = useTemplateRef('username-ref')
const bioRef = useTemplateRef('bio-ref')

const errMsg = ref('')

async function handleUpdate() {
    const image = imageRef.value?.newImage
    const username = usernameRef.value?.newUsername.trim()
    const bio = bioRef.value?.newBio.trim() || "看我超级搭路"

    errMsg.value = ''

    if (!image) {
        errMsg.value = '头像不能为空'
    } else if (!username) {
        errMsg.value = '用户名不能为空'
    } else {
        const formdata = new FormData()
        formdata.append('username', username)
        formdata.append('bio', bio)
        if (image !== user.image) formdata.append('image', base64ToFile(image, 'profile.png'))

        try {
            const r = await api.post('/api/user/profile/update/', formdata)
            const data = r.data

            if (data.result === 'success') {
                user.setUserInfo(data)
                // reseed the bio draft
                if (bioRef.value) bioRef.value.newBio = data.bio
            } else {
                errMsg.value = data.result
            }
        } catch (err) {
            console.log(err)
        }
    }
}
</script>

<template>
    个人资料
    <div class="flex justify-center">
        <div class="card card-border w-120 bg-base-200 shadow-sm mt-[15vh]">
            <div class="card-body">
                <h3 class="card-title">编辑资料</h3>
                <Image ref="image-ref" :image="user.image"/>
                <Username ref="username-ref" :username="user.username"/>
                <Bio ref="bio-ref" :bio="user.bio" />

                <p v-if="errMsg" class="text-sm text-red-500">{{ errMsg }}</p>

                <div class="card-actions justify-end">
                    <button @click="handleUpdate" class="btn btn-vue">
                        更新
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>
