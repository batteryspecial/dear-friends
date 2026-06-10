<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps(['name'])
const newName = ref(props.name)

watch(() => props.name, c => {
    newName.value = c
})

defineExpose({
    newName
})
</script>

<template>
    <fieldset class="fieldset">
        <label for="new-name" class="label text-base">名字</label>
        <input v-model="newName" id="new-name" type="text" class="input w-full">
    </fieldset>
</template>

<style scoped>

</style>