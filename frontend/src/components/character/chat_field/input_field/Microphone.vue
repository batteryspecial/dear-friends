<script setup lang="ts">
import KeyboardIcon from '@/components/icons/keyboard.vue';
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { MicVAD } from '@ricky0123/vad-web';
import { float32ToInt16 } from '@/utils/audio';
import api from '@/js/http/api';

type ASRProcessingResponse = {
    result: string;
    text: string;
};

const isSpeaking = ref<boolean>(false);

const emit = defineEmits(['close', 'send', 'stop']);
const { color } = defineProps(["color"]);

let vadInstance: MicVAD | null = null;

const startRecording = async (): Promise<void> => {
    const baseUrl: string = "http://127.0.0.1:8000/static/frontend/vad/"; // change to http://127.0.0.1:8000/static/frontend/vad/ in prod
    try {
        vadInstance = await MicVAD.new({
            baseAssetPath: baseUrl,
            onSpeechStart: () => {
                isSpeaking.value = true;
                emit('stop');
            },
            onSpeechEnd: (audio: Float32Array) => {
                isSpeaking.value = false;
                const pcm16: ArrayBuffer = float32ToInt16(audio);
                sendToBackend(pcm16);
            },
            ortConfig: (ort) => {
                ort.env.wasm.wasmPaths = baseUrl;
                ort.env.logLevel = "error";
            },
            positiveSpeechThreshold: 0.8,
            negativeSpeechThreshold: 0.65,
            // 5 帧 × 32ms（16kHz/512 采样每帧）
            minSpeechMs: 160,
            redemptionMs: 160,
        });
        await vadInstance.start();
    } catch (err) {
        console.error("VAD 初始化失败", err);
    }
};

const sendToBackend = async (arrayBuffer: ArrayBuffer): Promise<void> => {
    const blob = new Blob([arrayBuffer], { type: "audio/pcm" });
    const formData = new FormData();
    formData.append("audio", blob, "voice.pcm");

    try {
        const r = await api.post('/api/friend/message/asr/asr/', formData)
        const data: ASRProcessingResponse = r.data;
        if (data.result === 'success') {
            emit("send", null, data.text)
        }
    } catch (err) {
        console.log(err)
    }
};

onMounted(() => {
    startRecording()
})

onBeforeUnmount(() => {
    if (vadInstance) {
        vadInstance.destroy()
        vadInstance = null
    }
})
</script>

<template>
    <div @click="isSpeaking = !isSpeaking" class="absolute bottom-4 left-2 h-12 w-86 flex items-center rounded-2xl">
        <div
            class="w-full py-[7px] whitespace-pre-wrap break-words rounded-2xl bg-black/30 backdrop-blur-sm border !border-[color:var(--avg-color)] text-white text-base text-center"
            :style="{ '--avg-color': color }"
        >
            <div v-if="isSpeaking" class="flex items-center justify-center gap-1 h-6 flex-1">
                <div
                    v-for="i in 32" :key="i"
                    class="w-0.5 bg-blue-400 rounded-full animate-wave"
                    :style="{ animationDelay: `${i * 0.1}s` }"
                ></div>
            </div>
            <div v-else>
                语音输入
            </div>
        </div>
        <div @click="emit('close')" class="absolute right-2 w-8 h-8 flex justify-center items-center cusror-pointer">
            <KeyboardIcon />
        </div>
    </div>
</template>

<style lang="css" scoped>
.animate-wave {
  height: 4px;
  animation: wave-animation 0.6s ease-in-out infinite alternate;
}

@keyframes wave-animation {
  0% { height: 4px; opacity: 0.3; }
  100% { height: 20px; opacity: 1; }
}
</style>
