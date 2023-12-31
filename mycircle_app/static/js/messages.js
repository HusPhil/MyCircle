function autoResize() {
    const textarea = document.getElementById('message-input');
    textarea.style.height = 'auto'; // Reset the height to auto
    textarea.style.height = (textarea.scrollHeight) + 'px'; // Set the height to match the scroll height
}