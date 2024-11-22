import requests
import time

auth_key = '35bcb3940be849c898f1267ab61f8de1'
upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'
lemur_endpoint = 'https://api.assemblyai.com/lemur/v3/generate/summary'


headers_auth_only = {'authorization': auth_key}
headers = {
    "authorization": auth_key,
    "content-type": "application/octet-stream"
}
headers1 = {
    "authorization": auth_key,
    "content-type": "application/json"
}
CHUNK_SIZE = 5_242_880

fileName1 = 'AssemblyCreated'#For store name of generated files dynamically

# Function to upload audio
def upload(filename):
    def read_file(file_name):
        with open(file_name, 'rb') as f:
            while True:
                data = f.read(CHUNK_SIZE)
                if not data:
                    break
                yield data
    global fileName1
    fileName1 = filename
    upload_response = requests.post(upload_endpoint, headers=headers_auth_only, data=read_file(filename))
    return upload_response.json().get('upload_url')

# Function to transcribe audio
def transcribe(audio_url):
    transcript_request = {'audio_url': audio_url,
                          'auto_chapters':'true'}
                          
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers1)
    return transcript_response.json().get('id')

#Function to get the audio transcription
def get_text_of_audio(transcript_id):
    t_endpoint = f'https://api.assemblyai.com/v2/transcript/{transcript_id}'
    reqjason = requests.get(t_endpoint,headers=headers1)
    return reqjason.json()['text']

# Function to get summary using Lemur
def Lemur(transcript_id):
    lemur_request = {"transcript_ids": [transcript_id]}
    lemur_response = requests.post(lemur_endpoint, json=lemur_request, headers=headers1)
    return lemur_response.json().get('request_id')

# Function to poll summary
def poll_summary(request_id):
    polling_endpoint = f'https://api.assemblyai.com/lemur/v3/{request_id}'
    polling_response = requests.get(polling_endpoint, headers=headers1)
    return polling_response.json().get('response')

# Function to ask question about audio content,this uses the lemur model 
def askQA1(question, transcript_id):
    askQA1_endpoint = 'https://api.assemblyai.com/lemur/v3/generate/task'
    askQA_request = {
        "prompt":  question,
        "final_model": "anthropic/claude-3-5-sonnet",
        "max_output_size": 3000,
        "temperature": 0,
        "transcript_ids": [transcript_id]
    }
    L_response = requests.post(askQA1_endpoint, json=askQA_request, headers=headers1)
    
    return L_response.json()['response']

#poll the transcriotion function
def polling_transcription(t_id):
    polling_endpoint = f"{transcript_endpoint}/{t_id}"

    while True:
        status_response = requests.get(polling_endpoint,headers=headers1)
        status_jason = status_response.json()
        if(status_jason['status']=='completed'):
            print("Trasncsription completed")
            return status_jason
        elif (status_jason['status'] == 'failed'):
            print("Transcription failed.")
            return None
        else:
            print("Transcription is still processing. Waiting...")
            
            time.sleep(5)  # Wait for 5 seconds before polling again