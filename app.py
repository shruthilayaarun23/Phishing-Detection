import numpy as np
from flask import Flask,request,jsonify,render_template
from flask_cors import CORS
import pickle
import inputscript
app=Flask(__name__)
CORS(app)
model=pickle.load(open('Phishing_Website.pickle.dat','rb'))
@app.route('/predict',methods=['GET'])
def predict():
    args=request.args
    url = args.get('URL')
    return render_template('final.html')
@app.route('/ypredict',methods=['POST'])
def y_predict():
    url=request.form['URL']
    checkprediction=inputscript.featureExtraction(url)
    prediction=model.predict(checkprediction)
    print(prediction)
    output=prediction[0]
    if output==1:
        pred="This is a legitimate website"
    else:
        pred="This site is unsafe"
    #return render_template('final.html',prediction_text='{}'.format(pred),url=url)
    return {
        URL : url,
        Status : pred
        }
@app.route('/predict_api',methods=['POST'])
def predict_api():
    data=request.get_json(force=True)
    prediction=model.y_predict([np.array(list(data.values()))])
    output=prediction[0]
    return jsonify(output)
if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)