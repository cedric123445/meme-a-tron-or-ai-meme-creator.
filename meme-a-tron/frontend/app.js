async function fetchIntro() {
    const response = await fetch('http://localhost:8000/intro');
    const data = await response.json();
    document.getElementById('intro').innerText = data.intro;
}

async function uploadImage() {
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];
    if (!file) return alert('Upload an image first!');

    const preview = document.getElementById('preview');
    preview.src = URL.createObjectURL(file);

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:8000/generate-meme/', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();

    const captionsList = document.getElementById('captions');
    captionsList.innerHTML = '';
    data.captions.forEach(caption => {
        const li = document.createElement('li');
        li.innerText = caption;
        captionsList.appendChild(li);
    });
}

fetchIntro();