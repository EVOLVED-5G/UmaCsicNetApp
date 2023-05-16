from src.errors import bp
from flask import jsonify

# Base standard error
class AppErrorBaseClass(Exception):
    pass

# Object not found error
class ObjectNotFound(AppErrorBaseClass):
    pass

# Error handlers
@bp.app_errorhandler(Exception)
def handle_exception_error(e):
    return jsonify({'msg': 'Internal server error'}), 500

@bp.app_errorhandler(405)
def handle_405_error(e):
    return jsonify({'msg': 'Method not allowed'}), 405

@bp.app_errorhandler(403)
def handle_403_error(e):
    return jsonify({'msg': 'Forbidden error'}), 403
    
@bp.app_errorhandler(404)
def handle_404_error(e):
    return jsonify({'msg': 'Not Found error'}), 404
    
@bp.app_errorhandler(AppErrorBaseClass)
def handle_app_base_error(e):
    return jsonify({'msg': str(e)}), 500
    
@bp.app_errorhandler(ObjectNotFound)
def handle_object_not_found_error(e):
    return jsonify({'msg': str(e)}), 404