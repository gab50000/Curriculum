# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing

from datetime import datetime


db.define_table("curriculum",
                Field("u_id", "reference auth_user", default = auth.user_id),
                Field("datum", "date", default=datetime.today()),
                Field("picture", "upload"),
                Field("firstname", "string"),
                Field("surname", "string"),
                Field("adress", "string"),
                Field("telephone", "string"),
                Field("email", "string"),
                Field("recipient", "string"),
                Field("recipient_adress"),
                Field("opening", "string", default="Sehr geehrter Herr X"),
                Field("closing", "string", default="Mit freundlichen Grüßen,"),
                Field("story", "text")
                )

db.define_table("cvsection",
                Field("cv_id", "reference curriculum"),
                Field("title", "string"),
                Field("cvposition", "integer")
                )

db.define_table("cventry",
                Field("section_id", "reference cvsection"),
                Field("title", "string"),
                Field("description", "text")
                )

db.define_table("cvlistitem",
                Field("section_id", "reference cvsection"),
                Field("story", "text")
                )


db.curriculum.u_id.writable=False
db.curriculum.datum.writable=False
#db.applicant.cv_id.readable = db.cvsection.cv_id.readable = db.cvlistitem.section_id.readable = db.cventry.section_id.readable = db.job_application.cv_id.readable =False
db.cvsection.id.readable = db.cvlistitem.id.readable = db.cventry.id.readable = False
db.cvlistitem.section_id.writable = db.cventry.section_id.writable = db.cvsection.cv_id.writable = False
db.cvsection.cv_id.requires = IS_IN_DB(db, "curriculum.id")
db.cventry.section_id.requires = IS_IN_DB(db, "cvsection.id")
db.cvlistitem.section_id.requires = IS_IN_DB(db, "cvsection.id")
auth.enable_record_versioning(db)
