from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from product import api as product_ns
from auth import api as auth_ns  # also updated auth.py should use Namespace
 
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

# ✅ Initialize JWT and Swagger (via Flask-RESTX)
jwt = JWTManager(app)

api = Api(app, version='1.0', title='My API', description='Flask REST API with JWT & Swagger', doc='/docs')
app.route('/docs',methods=['Get'])
api.add_namespace(product_ns, path='/api')
api.add_namespace(auth_ns, path='/auth')

if __name__ == '__main__':
    app.run(debug=True)
