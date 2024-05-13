from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Post, post_schema, posts_schema

api = Blueprint('api',__name__, url_prefix='/api')
@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/posts', methods = ['POST'])
@token_required
def create_post(current_user_token):
    name = request.json['name']
    email = request.json['email']
    department = request.json['department'] 
    role = request.json['role']
    comment = request.json['comment']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    post = Post(name, email, department, role, comment, user_token = user_token )

    db.session.add(post)
    db.session.commit()

    response = post_schema.dump(post)
    return jsonify(response)

@api.route('/posts', methods = ['GET'])
@token_required
def get_post(current_user_token):
    a_user = current_user_token.token
    posts = Post.query.filter_by(user_token = a_user).all()
    response = posts_schema.dump(posts)
    return jsonify(response)

@api.route('/posts/<id>', methods = ['GET'])
@token_required
def get_single_post(current_user_token, id):
    post = Post.query.get(id)
    response = post_schema.dump(post)
    return jsonify(response)

@api.route('/posts/<id>', methods = ['POST','PUT'])
@token_required
def update_post(current_user_token,id):
    post = Post.query.get(id) 
    post.name = request.json['name']
    post.email = request.json['email']
    post.department = request.json['department']
    post.role = request.json['role']
    post.comment = request.json['comment']
    post.user_token = current_user_token.token
    db.session.commit()
    response = post_schema.dump(post)
    return jsonify(response)

@api.route('/posts/<id>', methods = ['DELETE'])
@token_required
def delete_post(current_user_token, id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    response = post_schema.dump(post)
    return jsonify(response)