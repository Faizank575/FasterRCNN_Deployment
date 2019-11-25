from flask import Flask, jsonify, request, make_response, send_file
from PIL import Image
import io,os,sys,base64,threading,uuid,pickle
from config import cfg
import cntk
from cntk import Trainer, load_model
from base64 import decodestring
import pickle
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import (UserRegister, User, UserLogin, UserUpdate,
                            CheckPhoneNumber,ForgetPassword,setNewPassword)
from resources.store import SubmissionList

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

app.config['DEBUG'] = True

POSTGRES = {
    'user': 'postgres',
    'pw': '',
    'db': 'SpikesApp',
    'host': 'localhost',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'faizank575'
api = Api(app)

jwt = JWTManager(app)  # not creating /auth


abs_path = os.path.dirname(os.path.abspath(__file__))
outputpath=os.path.join(abs_path, "CNTKModels")
model_path=os.path.join(outputpath, "spike.model")
print("Loading existing model from %s" % model_path)
loadedModel = load_model(model_path)
filename='./CNTKModels/regression_model.sav'
regressionModel=pickle.load(open(filename, 'rb'))


api.add_resource(SubmissionList, '/submissions')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserUpdate,'/updateProfile')
api.add_resource(CheckPhoneNumber,'/checkNumber')
api.add_resource(ForgetPassword, '/forgetPassword')
api.add_resource(setNewPassword, '/setNewPassword')
@app.route('/fasterRCNN/returnimage', methods=['POST'])
def return_image():
    content = request.values.getlist('image')
    username=request.values.get('username')
    image=base64.decodebytes(content[0].encode())
    img = Image.open(io.BytesIO(image))
    if img:
        temp_file_path=os.path.join(abs_path,'static',str(uuid.uuid4())+'.jpg')
        img.save(temp_file_path)
        app.logger.debug('File is saved as %s', temp_file_path)
    from evaluate import evaluateimage
    x=threading.Thread(target=evaluateimage,
                        args=(app,temp_file_path,"returnimage",username,regressionModel,loadedModel,))
    x.start()
    return {"message":"Your image has been successfully recieved by server to process"},200



if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run('0.0.0.0', port=5000)
