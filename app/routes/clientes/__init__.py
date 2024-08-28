
#Módulos de Flask
from flask import Blueprint, render_template, request, redirect, url_for, abort, Response
import xlwt.Workbook

from app.models.cliente import Cliente
from app.extensions.db import db
from sqlalchemy import update, insert

import io
import xlwt

#Blueprint
clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@clientes_bp.route('index', methods = ['GET'])
def index():

    clientes = Cliente.query.all()
    list_arr = []

    for cli in clientes:
        json_arr = {
            'id': cli.id,
            'name': cli.name,
            'email': cli.email,
            'active': cli.active
        }

        list_arr.append(json_arr)

    return render_template('clientes/index.html', obj = list_arr)

@clientes_bp.route('new', methods = ['GET', 'POST'])
def new():
    return render_template('clientes/form.html')

@clientes_bp.route('edit/<int:id_cliente>', methods = ['GET', 'POST'])
def edit(id_cliente):
    if request.method == 'GET':

        cliente = Cliente.query.filter(Cliente.id == id_cliente).first()
        if cliente is not None:
            json_cliente = {
                'id': cliente.id,
                'name': cliente.name,
                'email': cliente.email,
                'active': cliente.active
            }

        return render_template('clientes/form.html', obj = json_cliente)
    
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        name = request.form['name']
        email = request.form['email']

        try:

            if id_cliente:
                #Si existe el id_cliente se actualiza el registro
                upd = update(Cliente) \
                    .values(
                        {
                            Cliente.name: name.strip().upper(),
                            Cliente.email: email.strip().upper()
                        }
                    ) \
                    .where(Cliente.id == id_cliente)

                db.session.execute(upd)
                db.session.commit()

            else: #se inserta un nuevo cliente

                ins = insert(Cliente) \
                    .values(
                        {
                            Cliente.name: name.strip().upper(),
                            Cliente.email: email.strip().upper(),
                            Cliente.active: True #por defecto activo
                        }
                    )
                
                db.session.execute(ins)
                db.session.commit()

            return redirect(url_for('clientes.index'))


        except Exception as e:
            abort(500)

@clientes_bp.route('ajax_exportar_clientes_xls', methods = ['GET'])
def ajax_exportar_clientes_xls():

    if request.method == 'GET':

        #Creamos el libro Excel y la hoja
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('clientes')

        #Creamos una salida estándar
        output = io.BytesIO()

        row_num = 0

        #Para el encabezado del Excel en la 1era fila (row_num = 0)
        columns = ['ID', 'NAME', 'EMAIL']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num])

        #Llamamos a la lista de clientes
        clientes = Cliente.query.filter(Cliente.active == True)
        for cli in clientes:
            row_num += 1

            id = str(cli.id)
            name = cli.name
            email = cli.email

            ws.write(row_num, 0, id)
            ws.write(row_num, 1, name)
            ws.write(row_num, 2, email)

        #guardamos el libro en la salida estándar
        wb.save(output)
        output.seek(0)

        response_headers = {
            'Content-Disposition': 'attachment; filename=clientes.xls'
        }
        response = Response(output, mimetype='application/ms-excel', headers=response_headers)

        return response
        