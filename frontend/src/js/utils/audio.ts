// audio.ts

let mediaSource: MediaSource | null = null;
let sourceBuffer: SourceBuffer | null = null;
let audioPlayer: HTMLAudioElement = new Audio(); // 全局播放器实例
let audioQueue: Uint8Array[] = [];               // 待写入 Buffer 的二进制队列
let isUpdating: boolean = false;                 // Buffer 是否正在写入

const processQueue = (): void => {
    if (isUpdating || audioQueue.length === 0 || !sourceBuffer || sourceBuffer.updating) {
        return;
    }

    const chunk = audioQueue.shift();
    if (!chunk) return
    isUpdating = true;

    try {
        sourceBuffer.appendBuffer(chunk as BufferSource);
    } catch (e) {
        console.error("SourceBuffer Append Error:", e);
        isUpdating = false;
    }
};

export const teardownAudio = (): void => {
    audioPlayer.pause();
    audioPlayer.src = '';
}

export const stopAudio = (): void => {
    audioPlayer.pause();
    audioQueue = [];
    isUpdating = false;

    if (mediaSource) {
        if (mediaSource.readyState === 'open') {
            try {
                mediaSource.endOfStream();
            } catch (e) {
                console.log(e)
            }
        }
        mediaSource = null;
    }

    if (audioPlayer.src) {
        URL.revokeObjectURL(audioPlayer.src);
        audioPlayer.src = '';
    }
};

export function initAudioStream(): void {
    audioPlayer.pause();
    audioQueue = [];
    isUpdating = false;

    mediaSource = new MediaSource();
    audioPlayer.src = URL.createObjectURL(mediaSource);

    mediaSource.addEventListener('sourceopen', () => {
        try {
            if (mediaSource) {
                sourceBuffer = mediaSource.addSourceBuffer('audio/mpeg');
                sourceBuffer.addEventListener('updateend', () => {
                    isUpdating = false;
                    processQueue();
                });
            }
        } catch (e) {
            console.error("MSE AddSourceBuffer Error:", e);
        }
    });
    audioPlayer.play().catch((e: Error) => console.error("等待用户交互以播放音频", e));
}

export function handleAudioChunk(base64Data: string): void {
    // 将语音片段添加到播放器队列中
    try {
        const binaryString = atob(base64Data);
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }

        audioQueue.push(bytes);
        processQueue();
    } catch (e) {
        console.error("Base64 Decode Error: ", e);
    }
}
