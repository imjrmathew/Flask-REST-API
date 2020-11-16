# Necessary imports
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import User, Product, db
import jwt, base64
import cloudinary
import cloudinary.uploader
import cloudinary.api
from io import BytesIO
from dotenv import load_dotenv
from PIL import Image
from functools import wraps
import os



# Creating an app
app = Flask(__name__)


# Flask Configuration
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('TRACK','TRACK_MODIFICATIONS')
app.secret_key =os.environ.get('SECRET','SECRET_KEY')

cloudinary.config( 
    cloud_name = os.environ.get('CLOUD'), 
    api_key = os.environ.get('APIKEY'), 
    api_secret = os.environ.get('APISECRET')
)

# cloudinary.config(    
#     cloud_name = os.environ['CLOUD_NAME'], 
#     api_key = os.environ['API_KEY'], 
#     api_secret = os.environ['API_SECRET']
# )



# JWT Token Validation
# It Checks, whether there is token in header or not!
def token_required(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:  # checks weather token is passed in header
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'valid token is missing'})
        try:
            data = jwt.decode(token, app.secret_key)
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})
        return f(*args, **kwargs)
    return wrapped_function




""" 
This API is used for registering new user
It should contain following parameters, 
username, password, email, name.
"""

@app.route('/register' , methods=['POST'])
def register():
    data_obtained = request.get_json()
    if User.query.filter_by(username=data_obtained['username'], 
                            email=data_obtained['email']).first():
        return {"error": "User already exists!"}
    user = User(name=data_obtained['name'],
            username=data_obtained['username'], 
            password=generate_password_hash(data_obtained['password']),
            email=data_obtained['email'])
    db.session.add(user)
    db.session.commit()
    return {"message": "User Created!"}




""" 
This API is used to perform login operation
It should contain following parameters, 
username, password.
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    data_obtained = request.get_json()
    if not data_obtained or not data_obtained['username'] or not data_obtained['password']:
        return jsonify({'message': 'proper details regarding username and password not found'}), 401
    if User.query.filter_by(username=data_obtained['username']).first():
        user = User.query.filter_by(username=data_obtained['username']).first()
        if check_password_hash(user.password, data_obtained['password']):
            jwt_token = jwt.encode({'user_id': user.id}, app.secret_key)
            return jsonify({'token': jwt_token.decode('UTF-8')})
    return jsonify({'message': 'unable to verify'}), 401





""" 
This API is used for adding new product
It should contain following parameters, 
product_name, product_price and product_image.
"""

@app.route('/add', methods = ['POST'])
@token_required
def add_product():
    data_obtained = request.get_json()
    if Product.query.filter_by(product_name=data_obtained['product_name']).first():
        return {"error": "Product is already added!"}

    # Converting base64 image 
    file_binary_name = data_obtained['product_image']
    response = cloudinary.uploader.upload(file_binary_name)

    # Saving to database
    product_object = Product(product_name=data_obtained['product_name'], 
                            product_price=data_obtained['product_price'],
                            product_image=response['public_id'])
    db.session.add(product_object)
    db.session.commit()
    return {"message": "Product added successfully!"}




""" 
This API is used for view products
"""

@app.route('/view', methods = ['GET'])
@token_required
def view_product():
    product_data = Product.query.all()
    if product_data:
        return {"products": [x.json() for x in product_data]}
    return {"message": "There is no product!"}




""" 
This API is used to perform search operation
so, the url should contain id of the product
that we want to search.
"""

@app.route('/search/<int:id>', methods = ['GET', 'POST'])
@token_required
def view_single_product(id):
    product_data = Product.query.all()
    if Product.query.filter_by(id=id).first():
        product_data_only_one = Product.query.filter_by(id=id).first()
        return {"result": product_data_only_one.json()}
    return {"message": "There is no product!"}




""" 
This API is used for updating the product
It should contain following parameters, 
product_name, product_price, product_image.
"""

@app.route('/update/<int:id>', methods = ['GET', 'PUT'])
@token_required
def update_product(id):
    data_obtained = request.get_json()
    if Product.query.filter_by(id=id).first():
        product_data_update = Product.query.filter_by(id=id).first()
        
        # Converting base64 image 
        file_binary_name = data_obtained['product_image']
        image_cloudinary = cloudinary.api.resource(product_data_update.product_image)
        cloudinary.uploader.destroy(product_data_update.product_image)
        cloudinary.uploader.upload(file_binary_name, public_id=image_cloudinary['public_id'])

        # Updating to database
        product_data_update.product_name = data_obtained['product_name']
        product_data_update.product_price = data_obtained['product_price']

        db.session.add(product_data_update)
        db.session.commit()
        return {"message": "Updated Succesfully!"}
    return {"error": "There is no product!"}




""" 
This API is used for deleting a product
so, the url should contain id of the product
that we want to delete.
"""

@app.route('/delete/<int:id>', methods = ['GET', 'DELETE'])
@token_required
def delete_product(id):
    if Product.query.filter_by(id=id).first():
        product_data_delete = Product.query.filter_by(id=id).first()
        cloudinary.uploader.destroy(product_data_delete.product_image)
        db.session.delete(product_data_delete)
        db.session.commit()
        return {"message": "Deleted succesfully!"}
    return {"error": "There is no product!"}




# Main methods
if __name__ == '__main__':
    from models.models import db
    db.init_app(app)
    app.run(port=5000)