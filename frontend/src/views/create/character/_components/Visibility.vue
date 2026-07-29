<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps(['visibility']);
const newVisibility = ref(props.visibility);

watch(() => props.visibility, c => {
    newVisibility.value = c
})

defineExpose({
    newVisibility
})
</script>

<template>
    <label class="label">
        <input v-model="newVisibility" type="checkbox" class="toggle!" />
        Publish
    </label>
</template>

<style lang="css" scoped>

</style>
