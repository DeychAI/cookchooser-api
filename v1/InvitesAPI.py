from models import db, Invite, User
from flask.ext.restful import Resource, abort, fields, marshal, marshal_with, reqparse
from flask import g
from auth import auth
from v1.UserAPI import user_fields

invite_fields = {
    'id': fields.Integer,
    'from': fields.String(attribute='invite_from'),
    'to': fields.String(attribute='invite_to')
}


class InvitesListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('to', required = 'True')
        super(InvitesListAPI, self).__init__()

    # return list of invites that was sent to user
    @marshal_with(invite_fields)
    def get(self):
        return Invite.query.filter_by(invite_to=g.user.username).all()

    # sent new invite to the user
    @marshal_with(invite_fields)
    def post(self):
        args = self.parser.parse_args()
        user_to = User.query.filter_by(username=args['to']).first()
        if user_to is None:
            abort(400, message='User does not exist')

        invite = Invite.query.filter_by(invite_to=args['to'], invite_from=g.user.group).first()
        if invite is not None:
            abort(400, message="Invite for this user already sent")

        invite = Invite(invite_from = g.user.username, invite_to = args['to'])
        db.session.add(invite)
        db.session.commit()
        return invite, 201

    # delete all invites that was sent to user
    def delete(self):
        invites = Invite.query.filter_by(invite_to=g.user.group).all()
        for invite in invites:
            db.session.delete(invite)
        db.session.commit()
        return {'result': 'All invites deleted'}


class InviteAPI(Resource):
    decorators = [auth.login_required]

    #accept invite
    @marshal_with(user_fields)
    def post(self, inv_id):
        invite = Invite.query.filter_by(id=inv_id).first()
        if invite is None:
            abort(404, message="Invite not found")
        if invite.invite_to != g.user.group:
            abort(403, message="Access denied")

        g.user.group = invite.invite_from
        db.session.delete(invite)
        db.session.add(g.user)
        db.session.commit()
        return g.user

    # delete invite
    def delete(self, inv_id):
        invite = Invite.query.filter_by(id=inv_id).first()
        if invite is None:
            abort(404, message="Invite not found")
        if invite.invite_to != g.user.group:
            abort(403, message="Access denied")

        db.session.delete(invite)
        db.session.commit()
        return {'result': 'Invite deleted'}
