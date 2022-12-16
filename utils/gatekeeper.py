import os
from datetime import timedelta

import redis
from bcrypt import checkpw, gensalt, hashpw
from flask import jsonify
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token

jwt_redis_blocklist = redis.StrictRedis(
    host=os.getenv('REDIS_URI'), port=6379, db=0, decode_responses=True
)
ACCESS_EXPIRES = timedelta(hours=1)
TOKEN_EXPIRES = timedelta(days=7)
class GateKeeper():
  
    def check_if_token_is_revoked(self,jwt: dict):
        jti = jwt_payload["jti"]
        token_in_redis = jwt_redis_blocklist.get(jti)
        return token_in_redis is not None
    
    def revoke_token(self):
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
        return jsonify(msg="Access token revoked")
    
   
    def issue_token(self, identity):
        access_token = create_access_token(identity=identity, expires_delta=TOKEN_EXPIRES)
        return jsonify(access_token=access_token)
    
    def check_password(self,provided_pw, logged_pw):
        salt = gensalt(rounds=8, prefix=b"2b")
        self.provided_pw = hashpw(provided_pw.encode('utf-8'), salt)
        # provided_pw = provided_pw.decode()
        if logged_pw == provided_pw:
            return True
        else:
            return False
        
    def encrypt_password(self,plaintext_pw):
        salt = gensalt(rounds=8, prefix=b"2b")
        hashed  = hashpw(plaintext_pw.encode('utf-8'), salt)
        return hashed.decode()