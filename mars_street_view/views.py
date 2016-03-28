"""Establish view functions for Mars Street View web app."""
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
)


@view_config(route_name='home', renderer='templates/home.jinja2')
def home_view(request):
    """Home page view."""
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'mars-street-view'}

@view_config(route_name='rover', renderer='templates/rover.jinja2')
def rover_view(request):
    """Return appropriate pictures for a rover request."""
    try:
        rover = DBSession.query(Rover).filter(name == request.matchdict['rover_name'])
        sol = request.matchdict['sol']
        nav = rover.cameras.filter(name='NAVCAM')
        nav_today = nav.photos.filter(sol=sol)
    except:
        pass
        

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_mars-street-view_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
