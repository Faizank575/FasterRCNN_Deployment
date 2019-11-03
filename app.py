#!flask/bin/python
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
import sklearn
# from sklearn.linear_model import LinearRegression 

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

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'faizank575'
api = Api(app)

jwt = JWTManager(app)  # not creating /auth


@app.route('/', methods=['GET','POST'])
def index():
    return {"message":"successful"}

@app.route('/fetchData', methods=['GET','POST'])
def FetchData():


    return { 
        "submission" : [
                {"submissiontitle":"submission1",
                "submissionText":"Hello",
                "submissionYear":"2015"
                },
                {"submissiontitle":"submission2",
                "submissionText":"Hello2",
                "submissionYear":"2017"
                }
        ] },200

api.add_resource(SubmissionList, '/submissions')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserUpdate,'/updateProfile')
api.add_resource(CheckPhoneNumber,'/checkNumber')
api.add_resource(ForgetPassword, '/forgetPassword')
api.add_resource(setNewPassword, '/setNewPassword')


abs_path = os.path.dirname(os.path.abspath(__file__))
outputpath=os.path.join(abs_path, "CNTKModels")
model_path=os.path.join(outputpath, "spike.model")
print("Loading existing model from %s" % model_path)
loadedModel = load_model(model_path)
filename='./CNTKModels/regression_model.sav'
regressionModel=pickle.load(open(filename, 'rb'))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


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
    x=threading.Thread(target=evaluateimage,args=(app,temp_file_path,"returnimage",username,regressionModel,loadedModel,))
    x.start()
    return {"message":"Your image has been successfully recieved by server to process"},200



def convert_and_save(b64_string):
    with open("./Temp/imageToSave.jpg", "wb") as fh:
        fh.write(base64.decodebytes(b64_string.encode()))



@app.route('/upload_test', methods=['POST'])
def image_upload():
    content = request.values.getlist('image')
    print(content[0])
    convert_and_save(content[0])

    return({'message':'file_uploaded'})



@app.route('/another_upload_test', methods=['POST'])
def another_image_upload():
    content = request.values.getlist('image')
    print(content[0])
    image=base64.decodebytes(content[0].encode())
    img = Image.open(io.BytesIO(image))
    # image = Image.fromstring('RGB',(800,800),decodestring(content[0]))
    img.save("foo.png")
    

    return({'message':'file_uploaded'})


if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run('0.0.0.0', port=5000)
