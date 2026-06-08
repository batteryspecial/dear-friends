<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps(['bio'])
const newBio = ref(props.bio)

watch(() => props.bio, c => {
    newBio.value = c
}, { immediate: true })

defineExpose({
    newBio,
})
</script>

<template>
    <fieldset class="fieldset">
        <label class="label text-base">简介</label>
        <textarea v-model="newBio" rows="6" type="text" class="textarea w-full"></textarea>
    </fieldset>
</template>

<style scoped>

</style>
