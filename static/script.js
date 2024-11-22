const uploadForm = document.getElementById('uploadForm');
const summaryBtn = document.getElementById('summaryBtn');
const getTrancribe = document.getElementById('getTrancribe')
const askBtn1 = document.getElementById('askBtn1');
const autoBtn = document.getElementById('autoBtn')
const downloadBtn = document.getElementById('downloadBtn')
const loader = document.getElementById("loader");


uploadForm.onsubmit = async (e) => {
    e.preventDefault();
    // Show loading animation and hide any previous output
    loader.style.display = "block";
    document.getElementById('transcriptId').innerText = `uploading......`;
    const file = document.getElementById('fileInput').files[0];
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    loader.style.display = "none";
    document.getElementById('transcriptId').innerText = `Transcript ID: ${data.transcript_id}`;
};


//Send and Recive the data from the transcribe_audio function
getTrancribe.onclick = async () => {
    loader.style.display = "block";
    const transcriptId = document.getElementById('transcriptId').innerText.split(': ')[1];
    const response = await fetch('/text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript_id: transcriptId })
    });
    const data = await response.json();
    loader.style.display = "none";
    document.getElementById('getTrancribedbtn').innerText = `Audio Transcribe-: ${data.text}`;
}



//Send and Recive the data from the get_summary function
summaryBtn.onclick = async () => {
    loader.style.display = "block";
    document.getElementById('summeryid').innerText = `Generating......`;
    const transcriptId = document.getElementById('transcriptId').innerText.split(': ')[1];
    const response = await fetch('/summary', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript_id: transcriptId })
    });
    const data = await response.json();
    loader.style.display = "none";
    document.getElementById('summeryid').innerText = `Completed`;
    document.getElementById('summary').innerText = `Summary: ${data.summary}`;

};

//Send and Recive the data from the ask_question1 function
askBtn1.onclick = async () => {
    loader.style.display = "block";
    document.getElementById('AskQ').innerText = `Generating......`;
    const question = document.getElementById('questionInput1').value;
    const transcriptId = document.getElementById('transcriptId').innerText.split(': ')[1];

    const response = await fetch('/ask1', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question, transcript_id: transcriptId })
    });

    const data = await response.json();
    loader.style.display = "none";
    document.getElementById('AskQ').innerText = `Completed`;
    document.getElementById('answer1').innerText = `Answer:${data.answer1}`;


};
//Send and Recive the data from the autochapter function
autoBtn.onclick = async () => {
    loader.style.display = "block";
    document.getElementById('Chapter').innerText = `Generating........`;
    const transcriptId = document.getElementById('transcriptId').innerText.split(': ')[1];
    const response = await fetch('/askcapter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript_id: transcriptId })

    });
    const data = await response.json();
    loader.style.display = "none";
    document.getElementById('Chapter').innerText = `Completed`;


    const savedAnswerContainer = document.getElementById('savedAnswer');

    const response1 = await fetch('/get_saved_answer');
    const data1 = await response1.json();

    if (data1.error) {
        savedAnswerContainer.innerHTML = `<p style="color: red;">Error: ${data1.error}</p>`;
    } else {
        const formattedOutput = data1.map(item => {
            // Insert line breaks explicitly in summaries and gists
            const gist = item.gist ? item.gist.replace(/\n/g, '<br>') : 'Conclusion';
            const summary = item.summary
                ? item.summary.replace(/(?:\.|\n)(\s|$)/g, '.<br>')
                : 'Conclusion';

            return `<div>
                        <strong style='font-size:25px;'>&#128392;</strong> ${gist}<br>
                        <strong style='font-size:25px;'>&#x1F449;</strong> ${summary}
                    </div>`;
        }).join('<br>'); // Add spacing between entries

        savedAnswerContainer.innerHTML = formattedOutput;
    }

};

//handle the downloading
downloadBtn.onclick = async () => {

    // Fetch the dynamic file name from the server
    const response = await fetch('/get_filename');
    const data = await response.json();

    // Use the retrieved file name to download
    const dynamicFileName = data.filename;
    window.location.href = `/download/${dynamicFileName}`;


};

//handle the dropdown section
document.querySelectorAll('.faq-title').forEach(button => {
    button.addEventListener('click', () => {
        const content = button.nextElementSibling;
        const allContents = document.querySelectorAll('.faq-content');
        const question = button.querySelector('.faq-question');
        const toggle = button.querySelector('.faq-emoji');

        // Close all other open FAQs
        allContents.forEach(item => {
            if (item !== content) {
                item.style.maxHeight = null;
            }
        });

        // Toggle current FAQ
        if (content.style.maxHeight) {
            content.style.maxHeight = null;
            question.textContent = "Click to Open";
            toggle.textContent = '+';

        } else {
            content.style.maxHeight = content.scrollHeight + "px";
            question.textContent = "Click to Close";
            toggle.textContent = '-';

        }
    });
});
