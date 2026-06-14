<script setup lang="ts">
import CameraIcon from '@/views/user/profile/_components/icon/camera.vue';
import { ref, watch, useTemplateRef, onBeforeUnmount, nextTick } from 'vue';
import Croppie from 'croppie';

const props = defineProps(['bg'])
const newBackground = ref(props.bg)
const isHovered = ref(false)

watch(() => props.bg, c => {
    newBackground.value = c
})

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')

let croppie: Croppie | null = null

watch(() => props.bg, c => {
    newBackground.value = c
}, { immediate: true })

async function openModal(image: string) {
    modalRef.value?.showModal()
    await nextTick()

    if (!croppie) {
        if (!croppieRef.value) return

        croppie = new Croppie(croppieRef.value, {
            viewport: { width: 300, height: 500, type: "square" },
            boundary: { width: 600, height: 600 },
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

    newBackground.value = await croppie.result({
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
    newBackground
})
</script>

<template>
    <fieldset class="fieldset">
        <label class="label text-base">聊天背景</label>
        <div class="border-y-1 border-[#464e57] py-4 flex justify-center">
            <div class="avatar relative"
                @mouseenter="isHovered=true"
                @mouseleave="isHovered=false"
            >
                <div v-if="newBackground" class="w-60 h-100 rounded-box">
                    <img :src="newBackground" alt="角色背景图片">
                </div>
                <div v-else class="w-60 h-100 rounded-box bg-base-300 dark:bg-slate-300"></div>
                <Transition name="fade">
                    <div v-if="isHovered" @click="fileInputRef?.click()" class="absolute top-0 w-60 h-100 flex justify-center items-center bg-black/20 rounded-box cursor-pointer">
                        <CameraIcon />
                    </div>
                </Transition>
            </div>
            <input @change="onFileChange" ref="file-input-ref" type="file" accept="image/*" class="hidden">
        </div>

        <dialog id="image_modal" ref="modal-ref" class="modal">
            <div class="modal-box transition-none w-6/7 max-w-2xl">
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
    </fieldset>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
    transition: opacity 0.1s ease;
}
.fade-enter-from, .fade-leave-to {
    opacity: 0;
}
</style>