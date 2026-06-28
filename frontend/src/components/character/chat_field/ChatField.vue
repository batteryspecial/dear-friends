<script setup lang="ts">
import type { Friend } from '@/views/create/CreateIndex.vue';
import { useTemplateRef, computed, ref } from 'vue';
import InputField from './input_field/InputField.vue';
import CharacterImageField from './image_field/CharacterImageField.vue';

const props = defineProps(["friend", "color"]) as {
    friend: Friend,
    color: string
}
const modalRef = useTemplateRef("modal-ref")
const opened = ref(false)

function showModal() {
    modalRef.value?.showModal()
    requestAnimationFrame(() => { opened.value = true })
}

const bgStyle = computed(() => {
    const friend: Friend = props.friend;
    return friend
        ? { backgroundImage: `linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.25)), url(${friend.character.bg_image})` }
        : {}
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
            <form method="dialog" class="absolute top-0 right-0 z-10">
                <button class="btn btn-md btn-circle btn-ghost absolute right-2 top-2">✕</button>
            </form>
            <InputField :color="props.color" />
            <CharacterImageField v-if="props.friend" :character="props.friend.character" />
        </div>
    </dialog>
</template>

<style scoped>

</style>
