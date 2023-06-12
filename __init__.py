from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import *
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO,send
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies
app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"]="devsenior"
app.config["SECURITY_PASSWORD_SALT"]="devsenior"
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:S%401989@localhost/colornote?charset=utf8"
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS']=True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']="nguyenvanchien1999prohehe@gmail.com"
app.config['MAIL_PASSWORD']="skouzcyupkkoheny"
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

jwt=JWTManager(app)
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response
connected_clients = []
app.app_context().push()
mail=Mail(app)
db=SQLAlchemy(app)
socketIo=SocketIO(app,cors_allowed_origins="*")

