import os
import json

from flask import Flask, render_template, request, make_response, Blueprint
from flask_paginate import Pagination, get_page_parameter, get_page_args
import awsgi
import requests
import snowflake.connector
import base64
from base64 import decodestring

app = Flask(__name__)
# Research Blueprint
#mod = Blueprint('users', __name__)


conn = snowflake.connector.connect(
    user='IMLANIE',
    password='Roller2023!',
    account='rshhdih-kcb45053',
    role='ACCOUNTADMIN',
    # region='us-west-2',
    warehouse='COMPUTE_WH',
    database='SAMPLE'

)


# https://pythonhosted.org/Flask-paginate/
@app.route('/xpaginate')
def paginate():
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)

    #users = User.find(...)
    users = []
    pagination = Pagination(page=page, total=users.count(),
                            search=search, record_name='users')
    # 'page' is the default name of the page parameter, it can be customized
    # e.g. Pagination(page_parameter='p', ...)
    # or set PAGE_PARAMETER in config file
    # also likes page_parameter, you can customize for per_page_parameter
    # you can set PER_PAGE_PARAMETER in config file
    # e.g. Pagination(per_page_parameter='pp')

    return render_template('users/index.html',
                           users=users,
                           pagination=pagination,
                           )

# https://stackoverflow.com/questions/33556572/paginate-a-list-of-items-in-python-flask


@app.route('/paginate')
def retrieve():
    # get_page_arg defaults to page 1, per_page of 10
    # page, per_page, offset = get_page_args()

    sql = "SELECT * FROM CUSTOMERS limit 100;"
    print(sql)

    cursor = conn.cursor()
    cursor.execute(sql)

    for chunk in cursor:

        fs = cursor.fetchmany(10)

    print(fs)

    return render_template('retrieveFile.html', fs=fs_for_render, pagination=pagination,
                           form="submitIt")

    # REPLACE THIS CODE WITH SNOWFLAKE CONN
    # connection = MongoClient()
    # db=connection.rheoML

    # # After the main query, you need to apply the per_page limit and offset
    # fs = gridfs.GridFS(db)

    # fs_for_render = fs.limit(per_page).offset(offset)

    # you can also add css_framework='bootstrap3' to Pagination for easy styling

#     search = False
#     q = request.args.get('q')
#     if q:
#         search = True
#     try:
#         page = int(request.args.get('page', 1))

#     except ValueError:
#         page = 1

#         List = fs.list()
#         i = (page-1)*PER_PAGE
#         List1 = List[i:i+5]


# pagination = Pagination(page=page, per_page=per_page, offset=offset,
#                         total=fs.count(), record_name='List')

# return render_template('retrieveFile.html', fs=fs_for_render, pagination=pagination,
#                        form="submitIt")

# for folder_name, subfolders, filenames in os.walk('/var/task'):
#     print(f'The current folder is {folder_name}')
#     for subfolder in subfolders:
#         print(f'SUBFOLDER OF {folder_name}: {subfolder}')
#     for filename in filenames:
#         print(f'FILE INSIDE {folder_name}: {filename}')
#     print('')

# img = "./static/image"

# logo = 'snowflake.png'
# logo = base64.b64encode(logo).decode('utf-8')

# file = os.path.join(img, logo)
# print(type(file))
# curr_dir = os.getcwd()
# print("current working directory: " + curr_dir)

# print("image file exists?: ")
# print(os.path.exists("/var/task/static/image/snowflake.png"))


# with open("/var/task/static/image/snowflake.png", "rb") as f:
#     print("file found: ")

#     encodedPng = base64.b64encode(f.read())
#     # print(type(encodedPng))

#     # create a new image file
#     with open("/tmp/snowflake.png", "wb") as fh:
#         # fh.write(base64.decodebytes(encodedPng))
#         fh.write(decodestring(encodedPng))

#     # print(f)
#     # print(encodedPng)
#     # print(encodedPng.decode('utf-8'))
#     f.close()
#     fh.close()

# print("Snowflake.png file has been found and encoded")

# print("new image file exists in tmp dir?: ")
# print(os.path.exists("/tmp/snowflake.png"))
# # print(encodedZip.decode())


# for folder_name, subfolders, filenames in os.walk('/tmp'):
#     print(f'The current folder is {folder_name}')
#     for subfolder in subfolders:
#         print(f'SUBFOLDER OF {folder_name}: {subfolder}')
#     for filename in filenames:
#         print(f'FILE INSIDE {folder_name}: {filename}')
#     print('')


# print("Snowflake Connector Imported OK")


# sql = "select * from TPCH_SF10.CUSTOMER where C_PHONE='18-493-856-5843';"
# #sql = "select * from TPCH_SF10.CUSTOMER where C_CUSTKEY = "
# #customer_key = 165008
# #customer_key = str(customer_key)
# #sql = sql + customer_key

# cursor = conn.cursor()
# cursor.execute(sql)
# #df = cursor.fetch_pandas_all()
# result = cursor.fetchmany(10000)

# print(result)

# cursor.close()

@app.route("/new_cookie")
def new_cookie():

    response = make_response("set user in cookies")
    response.set_cookie("mycookie", "username")
    return response


@app.route("/get_cookie")
def get_cookie():

    try:
        cookie_value = request.cookies.get("mycookie")
        print("get cookie executed successfully")

        print(cookie_value)

    except Exception as ex:
        print("Error: " + str(ex))


@app.route('/phone', methods=["GET", "POST"])
def phone():
    # return render_template('home.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
    event = request.environ.get("awsgi.event", {})
    print(event)

    sql = "SELECT * FROM CUSTOMERS WHERE "

    #phone_number = "'18-493-856-5843'"
    filterby = request.form['HTMLfilterby']
    equals = " = "

    filtervalue = request.form['HTMLfiltervalue']

    if filterby == 'C_ACCTBAL':
        filtervalue = filtervalue.strip()
    else:
        filtervalue = filtervalue.strip()
        filtervalue = "'" + filtervalue + "'"

    #filtervalue = "'" + filtervalue + "'"
    filtervalue = str(filtervalue)

    print("Data type of input")
    print(filtervalue)
    print(type(filtervalue))

    end = ";"
    sql = sql + filterby + equals + filtervalue + end
    print(sql)

    cursor = conn.cursor()
    cursor.execute(sql)

    rows = cursor.fetchall()

    return render_template('home.html', data=rows)


@app.route('/home', methods=["GET", "POST"])
def home():
    # return render_template('home.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

    event = request.environ.get("awsgi.event", {})

    # with open("/var/task/static/image/snowflake.png", "rb") as f:
    #     print("file found: ")
    #     encodedPng = base64.b64encode(f.read())
    #     encodedPngnew = encodedPng.decode()
    #     print(encodedPng.decode())

    #     print(type(encodedPng))
    #     print(type(encodedPngnew))

    sql = "SELECT * FROM CUSTOMERS limit 1000;"
    print(sql)

    cursor = conn.cursor()
    cursor.execute(sql)

    rows = cursor.fetchmany(1000)
    # print(result)

    return render_template('home.html', data=rows)
    # cursor.close()


def lambda_handler(event, context):

    print("Lambda Flask Website Event: ")
    print(event)

    base64_content_types = [
        'image/vnd.microsoft.icon', 'image/x-icon', 'image/png']

    # can add extra info in response headers.  need to learn this
    return awsgi.response(app, event, context, base64_content_types)
