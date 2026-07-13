// 将 Float32 转 PCM 16-bit
export const float32ToInt16 = (float32Array: Float32Array): ArrayBuffer => {
    const buffer = new Int16Array(float32Array.length);
    float32Array.forEach((v, i) => {
        const s = Math.max(-1, Math.min(1, v));
        buffer[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
    });
    return buffer.buffer;
};
