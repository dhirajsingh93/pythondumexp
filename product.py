from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from utils import read_json, write_json

PRODUCTS_FILE = 'db/products.json'
api = Namespace('product', description='Product CRUD operations')

# ✅ Swagger model definition
product_model = api.model('Product', {
    'name': fields.String(required=True),
    'price': fields.Float(required=True)
})

# ✅ Optional: For response structure
product_response_model = api.inherit('ProductResponse', product_model, {
    'id': fields.Integer()
})

@api.route('/products')
class ProductList(Resource):
    @api.doc('get_all_products')
    @api.marshal_list_with(product_response_model)
    @jwt_required()
    def get(self):
        """Get all products"""
        return read_json(PRODUCTS_FILE)

    @api.expect(product_model)
    @api.doc('create_product')
  #  @jwt_required()
    def post(self):
        """Create a new product"""
        products = read_json(PRODUCTS_FILE)
        data = request.get_json()
        product = {
            "id": len(products) + 1,
            "name": data['name'],
            "price": data['price']
        }
        products.append(product)
        write_json(PRODUCTS_FILE, products)
        return {'msg': 'Product created'}, 201

@api.route('/products/<int:id>')
@api.param('id', 'The product identifier')
class ProductResource(Resource):
    @api.expect(product_model)
    @jwt_required()
    def put(self, id):
        """Update a product by ID"""
        products = read_json(PRODUCTS_FILE)
        product = next((p for p in products if p['id'] == id), None)
        if not product:
            return {'msg': 'Product not found'}, 404

        data = request.get_json()
        product['name'] = data.get('name', product['name'])
        product['price'] = data.get('price', product['price'])
        write_json(PRODUCTS_FILE, products)
        return {'msg': 'Product updated'}

    @jwt_required()
    def delete(self, id):
        """Delete a product by ID"""
        products = read_json(PRODUCTS_FILE)
        updated = [p for p in products if p['id'] != id]
        if len(updated) == len(products):
            return {'msg': 'Product not found'}, 404
        write_json(PRODUCTS_FILE, updated)
        return {'msg': 'Product deleted'}
