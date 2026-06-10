<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps(['desc'])
const newDesc = ref(props.desc)

watch(() => props.desc, c => {
    newDesc.value = c
})

defineExpose({
    newDesc
})
</script>

<template>
    <fieldset class="fieldset">
        <label for="new-description" class="label">角色介绍</label>
        <textarea v-model="newDesc" id="new-description" rows="6" class="textarea w-full max-h-67"></textarea>
    </fieldset>
</template>

<style scoped>

</style>