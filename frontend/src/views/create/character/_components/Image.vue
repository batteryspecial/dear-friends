<script setup lang="ts">
import { ref, useTemplateRef, watch, nextTick, onBeforeUnmount } from 'vue';
import CameraIcon from '@/views/user/profile/_components/icon/camera.vue';
import DefaultImage from './icons/default.vue'
import Croppie from "croppie";
import 'croppie/croppie.css';

const props = defineProps(['image'])
const newImage = ref(props.image)
const isHovered = ref(false)

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')

let croppie: Croppie | null = null

watch(() => props.image, c => {
    newImage.value = c
}, { immediate: true })

async function openModal(image: string) {
    modalRef.value?.showModal()
    await nextTick()

    if (!croppie) {
        if (!croppieRef.value) return

        croppie = new Croppie(croppieRef.value, {
            viewport: { width: 200, height: 200, type: "circle" },
            boundary: { width: 300, height: 300 },
            enableOrientation: true,
            enforceBoundary: true,
        })
    }

    croppie.bind({
        url: image,
    })
}

async function cropImage() {
    if (!croppie) return

    newImage.value = await croppie.result({
        type: 'base64',
        size: 'viewport',
    })

    modalRef.value?.close()
} 

const onFileChange = (e: Event) => {
    const target = e.target as HTMLInputElement

    if (target.files && target.files[0] && target.files.length > 0) {
        const file = target.files[0]
        target.value = ''

        const reader = new FileReader()
        reader.onload = () => {
            if (typeof reader.result === 'string') {
                openModal(reader.result)
            }
        }

        reader.readAsDataURL(file)
    }
}

onBeforeUnmount(() => {
    croppie?.destroy()
})

defineExpose({
    newImage,
})
</script>

<template>
    <div class="flex justify-center">
        <div class="avatar relative rounded-full! flex-col"
            @mouseenter="isHovered=true"
            @mouseleave="isHovered=false"
        >
            <div v-if="newImage" class="w-28 rounded-full">
                <img :src="newImage" alt="头像">
            </div>
            <div v-else class="w-28 h-28 rounded-full transition-none">
                <DefaultImage />
            </div>
            <Transition name="fade">
                <div v-if="isHovered" @click="fileInputRef?.click()" class="absolute left-0 top-0 w-28 h-28 flex justify-center items-center bg-black/20 rounded-full cursor-pointer">
                    <CameraIcon />
                </div>
            </Transition>
            <p class="text-center text-xs mt-2">点击修改角色头像</p>
        </div>
    </div>
    
    <input @change="onFileChange" ref="file-input-ref" type="file" accept="image/*" class="hidden">

    <dialog id="image_modal" ref="modal-ref" class="modal">
        <div class="modal-box transition-none w-6/7 max-w-xl">
            <form method="dialog">
                <button class="btn btn-md btn-circle btn-ghost absolute right-2 top-2">✕</button>
            </form>
            <div ref="croppie-ref" class="flex flex-col justify-center my-4"></div>
            <div class="modal-action">
                <button @click="modalRef?.close()" class="btn btn-outline">取消</button>
                <button @click="cropImage" class="btn btn-vue">确定</button>
            </div>
        </div>
    </dialog>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
    transition: opacity 0.1s ease;
}
.fade-enter-from, .fade-leave-to {
    opacity: 0;
}
</style>
