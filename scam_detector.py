def detect_scam(msg):
    keys=["otp","bank","upi","urgent","password","account"]
    return any(k in msg.lower() for k in keys)

app.py
------
from flask import Flask,request,jsonify
from flask_cors import CORS
import database, os
from scam_detector import detect_scam

app=Flask(__name__)
CORS(app)

database.init_db()
API_KEY=os.getenv("API_KEY")

@app.route('/auth',methods=['POST'])
def auth():
    if request.headers.get('x-api-key')!=API_KEY:
        return jsonify({'status':'unauthorized'}),401
    return jsonify({'status':'success'})

@app.route('/analyze',methods=['POST'])
def analyze():
    if request.headers.get('x-api-key')!=API_KEY:
        return jsonify({'status':'unauthorized'}),401

    d=request.json
    msg=d.get('message','')
    session=d.get('session_id','x')
    scam=detect_scam(msg)

    if scam:
        database.store(session,msg,'flagged')

    return jsonify({
        'status':'processed',
        'scamDetected':scam,
        'engagementMetrics':{'messages':1,'duration':0},
        'extractedIntelligence':[msg] if scam else [],
        'agentNotes':'analysis complete'
    })

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000)
