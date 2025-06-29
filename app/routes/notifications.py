from flask import request, Blueprint, jsonify
from ..schema.models import db, Notification
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..constants.http_status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND

# create a blueprint for this route
notification_bp = Blueprint('notifications', __name__, url_prefix='/api/v1.0/notifications')

# get all notificatons
@notification_bp.route('/')
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()

    if not notifications or notifications == '':
        return jsonify({'message': 'You do not have any notification.'}), HTTP_200_OK
    
    notifications_data = []
    count = len(notifications)
    for notification in notifications:
        notifications_data.append({
            'id' : notification.id,
            'message' : notification.message,
            'created_at' : notification.created_at,
            'is_read': notification.is_read
        })
    return jsonify({'notifications': notifications_data, 'count': count}), HTTP_200_OK

# read notification
@notification_bp.route('/<int:notification_id>/read')
@jwt_required()
def read_notification(notification_id):
    user_id = get_jwt_identity()

    notification = Notification.query.filter_by(user_id=user_id, id=notification_id).first()

    if not notification:
        return jsonify({'error': 'Notification not found.'}), HTTP_404_NOT_FOUND
    # mark notification as read
    if notification.is_read == 'false' or notification.is_read == False:
        notification.is_read = True
        db.session.commit()
        
    return jsonify({
        'notification':{
            'id': notification.id,
            'message': notification.message,
            'created_at': notification.created_at,
            'is_read': notification.is_read
        }
    }), HTTP_200_OK

# delete notification
@notification_bp.route('/<int:notification_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    user_id = get_jwt_identity()

    notification = Notification.query.filter_by(user_id=user_id, id=notification_id).first()

    if not notification:
        return jsonify({'error': 'Notification not found.'}), HTTP_404_NOT_FOUND
    
    if request.method == 'DELETE':
        # delete notification
        db.session.delete(notification)
        db.session.commit()
        return jsonify({'message': 'Notification deleted successfully.'}), HTTP_200_OK
    return None

# Mark all as read
@notification_bp.route('/mark_as_read', methods=["PUT"])
@jwt_required()
def mark_all_notifications():
    user_id = get_jwt_identity()

    notifications = Notification.query.filter_by(user_id=user_id).all()
    count = len(notifications)

    if not notifications or notifications == '':
        return jsonify({'message': 'You do not have any notifications.'}), HTTP_200_OK
    
    notifications_data = []

    if request.method == "PUT":
        for notification in notifications:
            if notification.is_read == 'false' or notification.is_read == False:
                # then set it to true to mark it as read
                notification.is_read = True
                db.session.commit()

                notifications_data.append({
                    'id' : notification.id,
                    'message' : notification.message,
                    'created_at' : notification.created_at,
                    'is_read': notification.is_read
                })
        return jsonify({'notifications': notifications_data, 'count': count}), HTTP_200_OK


