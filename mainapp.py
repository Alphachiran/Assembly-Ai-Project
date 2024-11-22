from flask import Flask, render_template, request, jsonify,send_file
from jsonTo_pdf import pdf_generator
from json_merge import process_and_save_json
from app_function import upload,transcribe,get_text_of_audio,Lemur,poll_summary,askQA1,polling_transcription,fileName1
import json
import os


app = Flask(__name__)
fileName1
# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

#For upload the file  
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    file = request.files['file']
    file.save(file.filename)
    audio_url = upload(file.filename)
    transcript_id = transcribe(audio_url)
    return jsonify({'transcript_id': transcript_id})

#Tigger the transcribe function and return the transcript_id
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    audio_url = request.json['audio_url']
    transcript_id = transcribe(audio_url)
    return jsonify({'transcript_id': transcript_id})

#Tigger the get_text_of_audio function and return the full transcription of audio content
@app.route('/text', methods= ['POST'])
def get_text():
    t_id = request.json['transcript_id']
    transcript_data= polling_transcription(t_id)
    if transcript_data is None:
        return jsonify({'text':"Transcription process has fail"})
    else:

        t = get_text_of_audio(t_id)
        return jsonify({'text': t})
    
tigger = False #this check the get_summer function get tigged or not

#Tigger the Lemur function to get the request id and then tigger the poll_summary function to return the summery,
#and save it as a jason file
@app.route('/summary', methods=['POST'])
def get_summary():
    global tigger
    tigger = True # Indicate Summery function get called first
    transcript_id = request.json['transcript_id']
    transcript_data = polling_transcription(transcript_id)
    if transcript_data is None:
        return jsonify({'summery':"Transcription process has fail"})
    else:
        request_id = Lemur(transcript_id)
        summary = poll_summary(request_id)
        filename = "summery"+fileName1+"summery.json"
        with open(filename,'w') as f:
            chapter = summary
            json.dump(chapter,f,indent=4)
        return jsonify({'summary': summary})

#Tigger the askQA1 funtion and return the Answer as json file
@app.route('/ask1', methods=['POST'])
def ask_question1():
    question = request.json['question']
    if question is None:
        return({'answer1':'Please enter a question'})
    transcript_id = request.json['transcript_id']
    if transcript_id is None:
        return({'answer1':'Please upload a file..'})
    transcript_data = polling_transcription(transcript_id)
    if transcript_data is None:
        return jsonify({'ansewr1': 'Transcription process failed'})
    else:
        a= askQA1(question, transcript_id)
        print("Trasncsription completed")
        return jsonify({'answer1':a})


#This is the function that created a full summery of the content
""" 
In here First check  whether the "summery function" get called and "summery.json" file saved or not.Then
using "transcribe function" request the chapters of the content and using "Lemur function" get the summery of 
the content and save those things in seperated json files.
Then using  "process_and_save_json function" create a nice looking full summery of the content using those 
seperated json fille and saved in merge json file
Then using "pdf_generator function" create a pdf file for download
"""
@app.route('/askcapter', methods=['POST'])
def autochapter():
    transcript_id = request.json['transcript_id']
    
    # Poll for the transcription result
    transcript_data = polling_transcription(transcript_id)
    if transcript_data is None:
        return jsonify({'error': "Transcription process failed"}), 500
    
    # Extract chapters from the transcription data
    chapters = transcript_data.get('chapters')
    if chapters is None:
        return jsonify({'error': "No chapters found in transcription"}), 404

#generating pdf and json section
    if(tigger):
        # Save chapters to a JSON file
        filename = "chapter"+fileName1+"chapter.json"
        with open(filename, 'w') as f:
            json.dump(chapters, f, indent=4)
        Text2 = "summery" + fileName1 + "summery.json"
        pdfFilename = "pdf"+fileName1
        pdf_generator(filename,Text2,pdfFilename)#create a pdf for full summery of the content
        process_and_save_json(filename,Text2,pdfFilename)#create a json file for full summery of the content 
        return jsonify({'message': "Chapters saved successfully"})
    
    else:#In here tigger the Lemur function and poll_summery funtion for generating summery first
        #to get the summery jason
        request_id = Lemur(transcript_id)
        summary = poll_summary(request_id)
        filename2 = "summery"+fileName1+"summery.json"
        with open(filename2,'w') as f:
            chapter = summary
            json.dump(chapter,f,indent=4)


        filename1 = "chapter"+fileName1+"chapter.json"
        with open(filename1, 'w') as f:
            json.dump(chapters, f, indent=4)
        
        pdfFilename = "pdf"+fileName1
        pdf_generator(filename1,filename2,pdfFilename)#create a pdf for full summery of the content
        process_and_save_json(filename1,filename2,pdfFilename)#create a json file for full summery of the content 
        return jsonify({'message': "Chapters saved successfully"})


#return the data of the content of the merge json file to the UI
@app.route('/get_saved_answer', methods=['GET'])
def get_saved_answer():
    filename = "mergepdf" + fileName1 + ".json"
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON file"}), 500

#download the pdf file
@app.route('/download/<filename>')
def download_file(filename):
    # Get the current directory
    directory = os.getcwd()  
    file_path = os.path.join(directory, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        return "Please upload the file first then click the Geneate full summery button", 404

    # Serve the file for download
    return send_file(file_path, as_attachment=True)

#send the name of the pdf file  
@app.route('/get_filename',methods=['GET'])
def get_filename():
    dynamic_filename =  "pdf"+fileName1+".pdf"
    return {"filename": dynamic_filename}

if __name__ == '__main__':
    app.run(debug=True) 