from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from app import genericRepository
from app.t_applications import forms as t_applicationsforms
from app.models import TRoles
from app.models import Bib_Organismes, CorRoles, TApplications
from app.utils.utilssqlalchemy import json_resp


route =  Blueprint('application',__name__)

@route.route('applications/list', methods=['GET','POST'])
def applications():
    entete = ['ID','Nom','Description', 'ID Parent']
    colonne = ['id_application','nom_application','desc_application','id_parent']
    contenu = TApplications.get_all(colonne)
    return render_template('affichebase.html', table = contenu, entete = entete, ligne = colonne, cheminM = "/application/update/", cle= "id_application", cheminS="/applications/delete/" )    

@route.route('application/add/new',defaults={'id_application': None}, methods=['GET','POST'])
@route.route('application/update/<id_application>',methods=['GET','POST'])
def addorupdate(id_application):
    form = t_applicationsforms.Application()
    form.id_parent.choices = TApplications.choixSelect('id_application','nom_application',1)
    if id_application == None:
        if request.method == 'POST': 
            if form.validate() and form.validate_on_submit():
                form_app = form.data
                if form.id_parent.data == -1:
                    form_app['id_parent'] = None
                form_app.pop('id_application')
                form_app.pop('csrf_token')
                form_app.pop('submit')
                TApplications.post(form_app)
                return redirect(url_for('application.applications'))
            else :
                flash(form.errors)
        return render_template('application.html', form= form)
    else :
        application = TApplications.get_one(id_application)
        form.id_parent.choices.remove((application['id_application'],application['nom_application'])) 
        if request.method == 'GET':
            if application['id_parent'] == None:
                    form.id_parent.process_data(-1)
            else:
                form.id_parent.process_data(application['id_parent'])
            form.nom_application.process_data(application['nom_application'])
            form.desc_application.process_data(application['desc_application'])  
        if request.method == 'POST':
            if form.validate_on_submit() and form.validate():
                form_app = form.data
                print('coucou2')
                if form.id_parent.data == -1:
                    form_app['id_parent'] = None
                form_app['id_application'] = application['id_application']
                form_app.pop('csrf_token')
                form_app.pop('submit')
                TApplications.update(form_app)
                return redirect(url_for('application.applications'))
            else :
                flash(form.errors)
        return render_template('application.html', form= form)
        



@route.route('applications/delete/<id_application>', methods=['GET','POST'])
def delete(id_application):
    TApplications.delete(id_application)
    return redirect(url_for('application.applications'))



#  NON UTILISE


# @route.route('/application', methods=['GET','POST'])
# def application():
#     form = t_applicationsforms.Application()
#     form.id_parent.choices = TApplications.choixSelect('id_application','nom_application',1)   
#     if request.method == 'POST': 
#         if form.validate() and form.validate_on_submit():
#             form_app = form.data
#             if form.id_parent.data == -1:
#                  form_app['id_parent'] = None
#             form_app.pop('id_application')
#             form_app.pop('csrf_token')
#             form_app.pop('submit')
#             TApplications.post(form_app)
#             return redirect(url_for('application.applications'))
#         else :
#             flash(form.errors)
#     return render_template('application.html', form= form )

# @route.route('applications/update/<id_application>', methods=['GET','POST'])
# def update(id_application):
#     entete = ['ID','Nom','Description', 'ID Parent']
#     colonne = ['id_application','nom_application','desc_application','id_parent']
#     contenu = TApplications.get_all(colonne)
#     # test
#     form = t_applicationsforms.Application()
#     application = TApplications.get_one(id_application)
#     tab = TApplications.choixSelect('id_application','nom_application',1)
#     tab.remove((application['id_application'],application['nom_application']))
#     form.id_parent.choices = tab
#     if request.method == 'GET':
#         print(form.id_parent.data)        
#         if application['id_parent'] == None:
#                 form.id_parent.process_data(-1)
#         else:
#             form.id_parent.process_data(application['id_parent'])  
#     if request.method == 'POST':
#         if form.validate_on_submit() and form.validate():
#             form_app = form.data
#             print('coucou2')
#             if form.id_parent.data == -1:
#                   form_app['id_parent'] = None
#             form_app['id_application'] = application['id_application']
#             form_app.pop('csrf_token')
#             form_app.pop('submit')
#             TApplications.update(form_app)
#             return redirect(url_for('application.applications'))
#         else :
#             flash(form.errors)
#     return render_template('affichebase.html', table = contenu, entete = entete, ligne = colonne, cheminM = "/applications/update/", cle= "id_application", cheminS="/applications/delete/", test ='application.html', form= form, nom_application = application['nom_application'], desc_application= application['desc_application'] )