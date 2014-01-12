# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

import os

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

@auth.requires_login()
def createcv():
    db.curriculum.insert(u_id=auth.user_id)

@auth.requires_login()
def deletecv():
#    cvcontent= db()
    return request.vars

@auth.requires_login()
def managecvs():
    #(auth.user_id == db.curriculum.u_id) & 
    # query = (db.applicant.cv_id == db.curriculum.id) & (db.job_application.cv_id == db.curriculum.id)
    selection=db(auth.user_id == db.curriculum.u_id).select(db.curriculum.id, db.curriculum.datum, orderby=db.curriculum.id)
    return dict(selection=selection)

# def editcv():
#     cvid=request.vars["cid"]

#     applicant=db(db.applicant.cv_id == cvid).select()
#     cvsection=db(db.cvsection.cv_id == cvid).select()
#     cventry=db(db.cventry.cv_id == cvid).select()
#     cvlistitem=db(db.cvlistitem.cv_id == cvid).select()
#     job_application=db(db.job_application.cv_id == cvid).select()

#     content=dict(applicant=applicant, cvsection=db.cvsection, cventry=db.cventry, cvlistitem=db.cvlistitem, job_application=db.job_application)

    # return dict(entries= content)
    # return dict(applicationform=applicationform, applicantform=applicantform)

def editcv():
    cvid=request.vars["cvid"]
    query = db.applicant.cv_id == cvid
    # & (db.cvsection.cv_id == cvid) & (db.job_application.cv_id == cvid)
    if db(query) == None:
        form = SQLFORM.grid(query, deletable=False, create=True, searchable=False, csv=False)
    else:
        applicant_ids = db(query).select(db.applicant.id)

        forms= [crud.read(db.applicant, appid["id"]) for appid in applicant_ids]


    return dict(forms = forms, q=db(query))

def editapplicant():
    cvid=request.vars["cid"]
    applicantform = SQLFORM.grid(db.applicant.cv_id == cvid)
    return dict(form = applicantform)

def newsection():
    form = crud.create(db.cvsection)
    return dict(form=form)

def createsection():
    pass
    # db.cvsection.

@cache.action()
def mydownload():
    if not session.counter:
        session.counter=1
    else:
        session.counter+=1
    path=os.path.join(request.folder,'private','testfile.txt')
    os.system("echo \""+str(session.counter)+" mal aufgerufen\" > "+path)
    return response.stream(path)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
