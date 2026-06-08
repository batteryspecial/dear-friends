export function base64ToFile(base64: string, filename: string): File {
    const arr = base64.split(',')
    if (arr.length < 2 || !arr[0] || !arr[1]) {
        throw new Error('Invalid Base64 / Data URL format');
    }

    const mimeMatch = arr[0].match(/:(.*?);/)
    if (!mimeMatch) {
        throw new Error('Could not parse MIME type from Data URL');
    }
    const mime = mimeMatch[1];

    const bstr = atob(arr[1])
    let n = bstr.length

    const u8arr = new Uint8Array(n)
    while (n--) u8arr[n] = bstr.charCodeAt(n)
        
    return new File([u8arr], filename, { type: mime })
}