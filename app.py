from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from sqlalchemy.exc import IntegrityError

from model import Session, SessionLocal, Provider, Activity
from logger import logger
from schemas import *

from flask_cors import CORS

# API setup
info = Info(title="TrakClub API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Tags
home_tag = Tag(name="Docs", description="API Documentation")
provider_tag = Tag(name="Provider", description="Manage clubs")
activity_tag = Tag(name="Activity", description="Manage activities")
session_tag = Tag(name="Session", description="Manage scheduled sessions")


# -------------------------
# HOME
# -------------------------
@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')


# -------------------------
# PROVIDER
# -------------------------
@app.post('/provider', tags=[provider_tag],
          responses={"200": ProviderViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_provider(form: ProviderSchema):
    try:
        provider = Provider(
            name=form.name,
            address=form.address,
            city=form.city,
            state=form.state,
            phone=form.phone,
            website=form.website,
            instagram=form.instagram,
            description=form.description
        )

        session = SessionLocal()
        session.add(provider)
        session.commit()

        logger.debug(f"Created provider: {provider.name}")

        return present_provider(provider), 200

    except IntegrityError:
        logger.warning("Provider already exists")
        return {"message": "Provider already exists"}, 409

    except Exception as e:
        logger.warning(f"Error creating provider: {e}")
        return {"message": "Could not create provider"}, 400


@app.get('/providers', tags=[provider_tag],
         responses={"200": ProviderListSchema})
def get_providers():
    session = SessionLocal()
    providers = session.query(Provider).all()

    return present_providers(providers), 200


@app.get('/provider', tags=[provider_tag],
         responses={"200": ProviderViewSchema, "404": ErrorSchema})
def get_provider(query: ProviderSearchSchema):
    session = SessionLocal()
    provider = session.query(Provider).filter(Provider.name == query.name).first()

    if not provider:
        logger.warning("Provider not found")
        return {"message": "Provider not found"}, 404

    return present_provider(provider), 200


@app.delete('/provider', tags=[provider_tag],
            responses={"200": ProviderDeleteSchema, "404": ErrorSchema})
def delete_provider(query: ProviderSearchSchema):
    provider_name = query.name

    session = SessionLocal()
    count = session.query(Provider).filter(Provider.name == provider_name).delete()
    session.commit()

    if count:
        logger.debug(f"Deleted provider: {provider_name}")
        return {"message": "Provider deleted", "name": provider_name}, 200
    else:
        logger.warning("Provider not found")
        return {"message": "Provider not found"}, 404

# -------------------------
# ACTIVITY
# -------------------------
@app.post('/activity', tags=[activity_tag],
          responses={"200": ActivitySchema, "409": ErrorSchema, "400": ErrorSchema})
def add_activity(form: ActivitySchema):
    try:
        activity = Activity(name=form.name)

        session = SessionLocal()
        session.add(activity)
        session.commit()

        logger.debug(f"Created activity: {activity.name}")

        return {"id": activity.id, "name": activity.name}, 200

    except IntegrityError:
        logger.warning("Activity already exists")
        return {"message": "Activity already exists"}, 409

    except Exception as e:
        logger.warning(f"Error creating activity: {e}")
        return {"message": "Could not create activity"}, 400


@app.get('/activities', tags=[activity_tag],
         responses={"200": ActivityListSchema})
def get_activities():
    session = SessionLocal()
    activities = session.query(Activity).all()

    return present_activities(activities), 200


@app.get('/activity', tags=[activity_tag],
         responses={"200": ActivitySchema, "404": ErrorSchema})
def get_activity(query: ActivitySchema):
    session = SessionLocal()
    activity = session.query(Activity).filter(Activity.name == query.name).first()

    if not activity:
        logger.warning("Activity not found")
        return {"message": "Activity not found"}, 404

    return {"id": activity.id, "name": activity.name}, 200


@app.delete('/activity', tags=[activity_tag],
            responses={"200": ActivityDeleteSchema, "404": ErrorSchema})
def delete_activity(query: ActivitySchema):
    activity_name = query.name

    session = SessionLocal()
    count = session.query(Activity).filter(Activity.name == activity_name).delete()
    session.commit()

    if count:
        logger.debug(f"Deleted activity: {activity_name}")
        return {"message": "Activity deleted", "name": activity_name}, 200
    else:
        logger.warning("Activity not found")
        return {"message": "Activity not found"}, 404
        
# -------------------------
# SESSION (scheduled offering)
# -------------------------
@app.post('/session', tags=[session_tag],
          responses={"200": SessionViewSchema, "400": ErrorSchema})
def add_session(form: SessionSchema):
    try:
        new_session = Session(
            weekday=form.weekday,
            time=form.time,
            provider_id=form.provider_id,
            activity_id=form.activity_id,
            name=form.name
        )

        db = SessionLocal()
        db.add(new_session)
        db.commit()

        logger.debug(f"Created session: {form.weekday} {form.time}")

        return present_session(new_session), 200

    except Exception as e:
        logger.warning(f"Error creating session: {e}")
        return {"message": "Could not create session"}, 400


@app.get('/sessions', tags=[session_tag],
         responses={"200": SessionListSchema})
def get_sessions():
    db = SessionLocal()
    rows = db.query(Session).all()

    return present_sessions(rows), 200


@app.get('/session', tags=[session_tag],
         responses={"200": SessionViewSchema, "404": ErrorSchema})
def get_session(query: SessionSchema):
    db = SessionLocal()

    row = db.query(Session).filter(
        Session.provider_id == query.provider_id,
        Session.activity_id == query.activity_id,
        Session.weekday == query.weekday,
        Session.time == query.time
    ).first()

    if not row:
        logger.warning("Session not found")
        return {"message": "Session not found"}, 404

    return present_session(row), 200


@app.delete('/session', tags=[session_tag],
            responses={"200": SessionDeleteSchema, "404": ErrorSchema})
def delete_session(query: SessionSchema):
    db = SessionLocal()

    count = db.query(Session).filter(
        Session.provider_id == query.provider_id,
        Session.activity_id == query.activity_id,
        Session.weekday == query.weekday,
        Session.time == query.time
    ).delete()

    db.commit()

    if count:
        logger.debug("Deleted session")
        return {"message": "Session deleted", "id": count}, 200
    else:
        logger.warning("Session not found")
        return {"message": "Session not found"}, 404