from flask import Blueprint, jsonify, redirect, url_for
from utils import login_required

user_blueprint = Blueprint('user', __name__, template_folder='./template', static_folder='./static')

@user_blueprint.route('/users/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'success', 
        'message': 'check'
    })

    