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
from collections import OrderedDict
from datetime import datetime
import random

def randomstring(length):
    return "".join(map(lambda x:str(unichr(x)), [random.randint(97, 122) for i in range(length)]))

@auth.requires_login()
def index():

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

# @auth.requires_login()
# def createcv():
#     db.curriculum.insert(u_id=auth.user_id)

@auth.requires_login()
def managecvs():
    form = SQLFORM.smartgrid(db.curriculum, linked_tables=["cvsection"])
    return dict(form=form)
    #(auth.user_id == db.curriculum.u_id) & 
    # query = (db.applicant.cv_id == db.curriculum.id) & (db.job_application.cv_id == db.curriculum.id)
    # selection=db(auth.user_id == db.curriculum.u_id).select(db.curriculum.id, db.curriculum.datum, orderby=db.curriculum.id)
    # return dict(selection=selection)

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
@auth.requires_login()
def editcv():
    cvid=request.args(0)
    # cvid=request.vars["cvid"]
    query = db.curriculum.id == cvid
    form= SQLFORM.grid(query, editable=True, csv=False, create=False, searchable=False)
    form2= SQLFORM(db.curriculum, cvid)
    arg=request.args(0)
    return dict(form = form, form2=form2, arg=arg)

def editapplicant():
    cvid=request.vars["cid"]
    form = SQLFORM.grid(db.applicant.cv_id == cvid, editable=True)
    return dict(form = form)

def delete_section():
    return dict()

def newsection():
    cvid=request.args(0)
    form = crud.create(db.cvsection)
    return dict(form=form)

@auth.requires_login()
def view_curriculum():
    db.curriculum.insert(u_id=auth.user_id, datum=datetime.today(), picture=None, firstname=randomstring(6), surname=randomstring(10), \
        adress=randomstring(15), telephone="".join(map(str, [random.randint(0,9) for i in range(8)])), email=randomstring(4)+"@"+randomstring(6)+".de", \
        recipient=randomstring(10), recipient_adress=randomstring(10), opening=randomstring(20), closing=randomstring(20), story=randomstring(400))

    sectionnumber = random.randint(0,5)

    for i in xrange(sectionnumber):
        db.cvsection.insert()

    return dict(form=SQLFORM.grid(db.curriculum.u_id == auth.user_id, editable =False))


@auth.requires_login()
def viewcomplete():
    cvid=request.args(0)
    currform = crud.update(db.curriculum, cvid)
    sections = db(db.cvsection.cv_id == cvid).select()
    #keys are the section.ids
    cventries = OrderedDict()
    cvlistitems = OrderedDict()
    cvsections= OrderedDict()

    for section in sections:
        cvsections[section.id] = crud.update(db.cvsection, section.id)

        cventries[section.id] = []
        cventry_rows = db(db.cventry.section_id == section.id).select()
        for cventry in cventry_rows:
            cventries[section.id].append(crud.update(db.cventry, cventry.id))

        cvlistitems[section.id] = []
        cvlistitem_rows = db(db.cvlistitem.section_id == section.id).select()
        for cvlistitem in cvlistitem_rows:
            cvlistitems[section.id].append(crud.update(db.cvlistitem, cvlistitem.id))

    return dict(curriculum = currform, cventries=cventries, cvlistitems=cvlistitems, cvsections=cvsections)

@auth.requires_login()
def viewcv():
    # cvid=request.args(0)
    cvid=1
    query = (db.curriculum.u_id == auth.user_id) & (db.cvsection.cv_id == db.curriculum.id) & (db.cventry.section_id ==\
           db.cvlistitem.section_id == db.cvitem.section_id == db.cvsection.id)
    form = SQLFORM.grid(query)#(db.cvsection.cv_id == db.curriculum.id) & (db.curriculum.u_id == auth.user_id) )
    return dict(form=form, cvid=cvid, uid=auth.user_id)


@cache.action()
def mydownload():
    if not session.counter:
        session.counter=1
    else:
        session.counter+=1
    path=os.path.join(request.folder,'private','testfile.txt')
    os.system("echo \""+str(session.counter)+" mal aufgerufen\" > "+path)
    return response.stream(path)

def cvform():
    return dict()

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
