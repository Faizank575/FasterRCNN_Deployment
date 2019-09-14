#!flask/bin/python
from flask import Flask, jsonify, request, make_response, send_file
import os,sys
import base64
# os.environ['PATH'] =os.environ['PATH']
import uuid
from config import cfg
import cntk
from cntk import Trainer, load_model
app = Flask(__name__)

abs_path = os.path.dirname(os.path.abspath(__file__))
# sys.path.append('C:\\Users\\FaizanKhan\\Anaconda3\\envs\\CNTK\lib\\site-packages\\cntk')
# sys.path.append(os.path.join(abs_path,'utils'))
# sys.path.append('C:\\Users\\FaizanKhan\\Anaconda3\\envs\\CNTK\lib\\site-packages\\cntk\\internal')

# print(sys.path)
# print(abs_path)
outputpath=os.path.join(abs_path, "CNTKModels")
model_path=os.path.join(outputpath, "spike.model")
# model_path = os.path.join(cfg["CNTK"].MODEL_DIRECTORY, cfg["CNTK"].MODEL_NAME)
print("Loading existing model from %s" % model_path)
# loadedModel=C.Function.load(model_path)
loadedModel = load_model(model_path)
# print("model loaded")

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/', methods=['GET','POST'])
def index():
    return {"message":"successful"}


@app.route('/hotelidentifier/api/v1.0/evaluate/returntags', methods=['POST'])
def return_tags():
    file_upload = request.files['file']
    if file_upload:
        temp_file_path=os.path.join('./Temp',str(uuid.uuid4())+'.jpg')
        file_upload.save(temp_file_path)
        app.logger.debug('File is saved as %s', temp_file_path)
    from evaluate import evaluateimage
    return jsonify(tags=[e.serialize() for e in evaluateimage(temp_file_path,"returntags",eval_model=loadedModel)])

@app.route('/hotelidentifier/api/v1.0/evaluate/returnimage', methods=['POST'])
def return_image():
    file_upload = request.files['file']
    if file_upload:
        temp_file_path=os.path.join('./Temp',str(uuid.uuid4())+'.jpg')
        file_upload.save(temp_file_path)
        app.logger.debug('File is saved as %s', temp_file_path)
    from evaluate import evaluateimage
    return send_file(evaluateimage(temp_file_path,"returnimage",eval_model=loadedModel), mimetype='image/jpg')
    #return send_file(os.path.join('./Temp', temp_filename), mimetype='image/jpg')
def convert_and_save(b64_string):
    with open("./Temp/imageToSave.jpg", "wb") as fh:
        fh.write(base64.decodebytes(b64_string.encode()))
@app.route('/upload_test', methods=['POST'])
def image_upload():
    content = request.values.getlist('image')
    print(content[0])
    convert_and_save(content[0])
    # file_upload = request.files['file']
    # print(file_upload)

    return({'message':'file_uploaded'})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)