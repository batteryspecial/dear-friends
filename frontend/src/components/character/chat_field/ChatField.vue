<script setup lang="ts">
import type { Friend } from '@/views/create/CreateIndex.vue';
import { useTemplateRef, computed } from 'vue';

const props = defineProps(["friend"])
const modalRef = useTemplateRef("modal-ref")

function showModal() {
    modalRef.value?.showModal()
}

const modalStyle = computed(() => {
    const friend: Friend = props.friend;
    if (friend) {
        return {
        backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.25)), url(${friend.character.bg_image})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        }
    } else {
        return {}
    }
})

defineExpose({
    showModal,
})
</script>

<template>
    <dialog ref="modal-ref" class="modal">
        <div class="modal-box w-90 h-150" :style="modalStyle">
            <form method="dialog" class="absolute top-1 right-1">
                <button class="btn btn-md btn-circle btn-ghost absolute right-2 top-2">✕</button>
            </form>
        </div>
    </dialog>
</template>

<style scoped>

</style>
