import mysql.connector
import json
from flask import Flask, jsonify, request

# ======================================================================================

app = Flask(__name__)

# ======================================================================================

@app.route("/")
def index():
    return "Hello VideoPoints!"

# ======================================================================================

@app.route('/users', methods=['POST'])
def create_user():

    posted_data = request.get_json()

    print (posted_data)
        
    tuple_params = tuple(posted_data.values())

    print (tuple_params)

    # connect to database

    mydb = mysql.connector.connect(
    host="127.0.0.1",
    #host = "db";
    port = "53306",
    user="vpUser",
    password="vpPassword!",
    database="vpdb"
    )

    # set insert cursor
    mycursor = mydb.cursor()

    query = "INSERT INTO users \
            (first_name, last_name, institution, email, phone_number, website_url, web_signature, \
            password, password_reset_on, account_locked, row_version, active, modified, created) \
            select \
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"

    # parameters = ('Peter', 'Parker', 'UT', 'spiderman@superheros.com', '1111111111', 'www.marvel.com', 
    # 'superhero', 'spiderman123', '2020-08-13', 0, 1, 1, '2020-08-13', '2020-08-13')

    mycursor.execute(query, tuple_params)

    mydb.commit()

    users_created = mycursor.rowcount

    mycursor.close()
    mydb.close()

    print(users_created)
    return "users_created: {}".format(users_created)

# ======================================================================================

@app.route("/users/<id>", methods=['GET'])
def get_user(id):

    print (id) 

    mydb = mysql.connector.connect(
    host="127.0.0.1",
    #host = "db";
    port = "53306",
    user="vpUser",
    password="vpPassword!",
    database="vpdb"
    )

    mycursor = mydb.cursor()

    mycursor.execute("select * from users where id = %s", (id, ))

    row_headers=[x[0] for x in mycursor.description] 

    rv = mycursor.fetchall()
    print (rv) 

    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    return json.dumps(json_data, indent=4, sort_keys=True, default=str)

# ======================================================================================

@app.route("/users", methods=['PUT'])
def update_user():

    posted_data = request.get_json()

    # print (posted_data)

    tuple_params = tuple(posted_data.values())

    print (tuple_params)

    # connect to database

    mydb = mysql.connector.connect(
    host="127.0.0.1",
    #host = "db";
    port = "53306",
    user="vpUser",
    password="vpPassword!",
    database="vpdb"
    )

    # set insert cursor
    mycursor = mydb.cursor()
    
    query = "UPDATE users SET \
    first_name = %s, \
    last_name = %s, \
    institution = %s, \
    email = %s, \
    phone_number = %s, \
    website_url = %s, \
    web_signature = %s, \
    password = %s, \
    password_reset_on = %s, \
    account_locked = %s, \
    row_version = %s, \
    active = %s, \
    modified = now() \
    WHERE id = %s"

    print (query)

    mycursor.execute(query, tuple_params)

    mydb.commit()

    user_updated = mycursor.rowcount

    mycursor.close()
    mydb.close()

    print(user_updated)
    return "user_updated: {}".format(user_updated)

# ======================================================================================

@app.route("/users", methods=['GET'])
def get_all_users():
    mydb = mysql.connector.connect(
    host="127.0.0.1",
    #host = "db";
    port = "53306",
    user="vpUser",
    password="vpPassword!",
    database="vpdb"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM users")

    row_headers=[x[0] for x in mycursor.description] 

    rv = mycursor.fetchall()

    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    mycursor.close()
    mydb.close()

    return json.dumps(json_data, indent=4, sort_keys=False, default=str)

# ======================================================================================

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):

    print (id)

    # connect to database

    mydb = mysql.connector.connect(
    host="127.0.0.1",
    #host = "db";
    port = "53306",
    user="vpUser",
    password="vpPassword!",
    database="vpdb"
    )

    # set insert cursor
    mycursor = mydb.cursor()
    
    query = "DELETE FROM users WHERE id = %s"

    params = (id, )

    print (query)

    mycursor.execute(query, params)

    mydb.commit()

    message = ""
    user_deleted = mycursor.rowcount
    if user_deleted == 1:
        message = "user successfully deleted"
    else:
        message = "error in user deletion"

    mycursor.close()
    mydb.close()

    return message
    
# ======================================================================================

if __name__ == "__main__":
    app.run()
