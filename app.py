import ast
import os
import uuid

from flask import Flask, render_template, request,session,redirect,url_for, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import constants
from decorators import check_admin_login, check_admin_or_swimmer
from lib.email import Mailer
from lib.hy3file import HY3file
from lib.linkgenerator import LinkGenerator
from lib.mongo import Mongo
from lib.objectmaker import Objectmaker

app = Flask(__name__)
app.secret_key = 'this is my fourth year software development project'
app.config['MAX_CONTENT_LENGTH'] = constants.MAX_UPLOAD_SIZE
db_config = {}
link_generator = LinkGenerator(app)
mailer = Mailer(app)


@app.route('/login',methods=['POST', 'GET'])
def login():
    print(request)
    if request.method == 'POST':
        username = request.form['inputUserName']
        password = generate_password_hash(request.form['inputPassword'])
        with Mongo(db_config) as db:
            data = db.admin.find_one({'username':username})
        if check_password_hash(password,data['password']):
            session['username']= username
            session["clubid"] = data["clubid"]
            return redirect(url_for('menu'))
    return redirect(url_for('main'))


@app.route('/logout')
@check_admin_login
def logout():
    if 'username' in session:
        session.pop('username')
        return redirect(url_for('main'))
    else:
        return redirect(url_for('main'))

@app.route("/menu")
def menu():
    return render_template('menu.html')


@app.route('/')
def main():
    return render_template('index.html')


def _is_allowed_file(filename):
    """ Check extensions if upload allowed """
    r = '.' in filename and filename.rsplit('.', 1)[1] in constants.UPLOAD_FILE_TYPES
    return r


def _save_file(file):
    if _is_allowed_file(file.filename):
        filename = secure_filename(str(uuid.uuid4()) + "_" + file.filename)
        file.save(os.path.join(constants.UPLOAD_PATH, filename))
        return filename
    else:
        raise InvalidFileTypeException('Invalid file type received.')


@app.route('/upload', methods=['GET', 'POST'])
@check_admin_login
def upload():

    if request.method == 'POST':
        if not "zip_file" in request.files:
            return "no zip file found"
        if not "mdb_file" in request.files:
            return "no mdb file found"

        try:
            zip_file = _save_file(request.files['zip_file'])
            mdb_file = _save_file(request.files['mdb_file'])
        except InvalidFileTypeException:
            return 'Invalid file type received, expected .zip and .mdb files. Please go back and try again'
        return _load_data_from_files(mdb_file, zip_file)
    else:
        return render_template('upload.html')



def _load_data_from_files(mdb_file, zip_file):
    try:
        o = Objectmaker(os.path.join(constants.UPLOAD_PATH, mdb_file), os.path.join(constants.UPLOAD_PATH, zip_file))
    except Exception as e:
        return render_template('output.html', data='Could not read mdb or zip file. <br/>Error: ' + str(e))
    data = o.get_data()
    swimmers = data.pop('swimmers')
    with Mongo(db_config) as db:
        db.gala.update_one({"title": data["title"],"club.id": data["club"]["id"]}, {'$set': data}, True)
        for swimmer in swimmers.values():
            db.swimmers.update_one({"swimmer_id": swimmer["swimmer_id"],"club_id": data["club"]["id"]}, {'$set': swimmer}, True)

    os.remove(os.path.join(constants.UPLOAD_PATH, mdb_file))
    os.remove(os.path.join(constants.UPLOAD_PATH, zip_file))

    for heat in data["heats"]:
        heat["id"] = int(heat["id"])
    return render_template("output.html", data=data)


@app.route('/send/<club_id>/<gala_id>')
@check_admin_login
def send_emails(club_id, gala_id):
    with Mongo(db_config) as db:
        #gala = db.gala.find_one({"title": gala_id, "club.id": club_id})
        swimmers = db.swimmers.find({"club_id": club_id})

    got_email = []
    no_email = []
    for swimmer in swimmers:
        link = constants.FORM_ADDRESS + link_generator.generate_payload(gala_id, club_id, swimmer['swimmer_id'])
        if not swimmer["inactive"]:
            if swimmer["email"] is None or swimmer["email"] == "":
                no_email.append({"swimmer" : swimmer, "link" : link})
            else:
                got_email.append({"swimmer" : swimmer, "link" : link})
                mailer.send_mail(swimmer["email"], 'Gala invitation.',
                                     render_template("link_mail.txt",first_name=swimmer["first"], link = link, club_id = club_id),
                                     render_template("link_mail.html",first_name=swimmer["first"], link = link, club_id = club_id))
    return render_template("sentemail.html", got_email=got_email, no_email=no_email, gala_id=gala_id)


@app.route('/form/<payload>')
def form(payload):
    decrypted_payload = link_generator.load_payload(payload)
    gala = decrypted_payload['gala_id']
    swimmer_id = decrypted_payload['swimmer_id']
    club_id = decrypted_payload['club_id']
    session['swimmer'] = swimmer_id
    with Mongo(db_config) as db:
        gala = db.gala.find_one({"title": gala, "club.id": club_id})
        swimmer = db.swimmers.find_one({'swimmer_id': swimmer_id, "club_id": club_id})
    gala = filter_heats(gala, swimmer)
    return render_template("form.html", swimmer=swimmer, gala=gala)



@app.route('/form/external/<gala_id>')
@check_admin_login
def external_form(gala_id):
    with Mongo(db_config) as db:
        gala = db.gala.find_one({'title': gala_id, "club.id":session['clubid']})
        swimmers = db.swimmers.find({"email" : None, "club_id":session['clubid'], "inactive":False})

    data = []
    for swimmer in swimmers:
        d = {
            "swimmer" : swimmer,
            "gala" :  filter_heats(gala, swimmer)
        }
        data.append(d)
    return render_template("multipleforms.html", data=data)



@app.route('/submit/<club_id>/<gala_id>/<swimmer_id>', methods=['POST'])
@check_admin_or_swimmer
def submit(club_id,gala_id, swimmer_id):
    if swimmer_id != session['swimmer']:
        return 'Error, invalid swimmer id detected'
    selected = request.form.getlist('selected')
    heats = []
    for heat in selected:
        v = ast.literal_eval(heat)
        v["id"] = str(v["id"])
        heats.append(v)
    with Mongo(db_config) as db:
        gala = db.gala.find_one({'title': gala_id, 'club.id': club_id})
        swimmer = db.swimmers.find_one({'swimmer_id': swimmer_id, 'club_id': club_id})
    entry = {
        'gala_id': gala_id,
        'swimmer_id': swimmer_id,
        'club_id': club_id,
        'heats': heats,
    }
    with Mongo(db_config) as db:
        db.entries.update_one({'gala_id': gala_id,'swimmer_id': swimmer_id, 'club_id': club_id}, {'$set': entry}, True)
    template = render_template("submitted.html", heats=heats, swimmer=swimmer, gala=gala)
    if swimmer["email"]:
        link = constants.FORM_ADDRESS + link_generator.generate_payload(gala_id, club_id, swimmer['swimmer_id'])
        mailer.send_mail(swimmer["email"], 'Gala invitation.',
                         body=render_template("confirmation_mail.txt", heats=heats, swimmer=swimmer, gala=gala, link=link),
                         html=render_template("confirmation_mail.html", heats=heats, swimmer=swimmer, gala=gala, link=link))
    return template

@app.route('/download/<gala_id>')
@check_admin_login
def download_file(gala_id):
    file = HY3file(gala_id, session['clubid']).to_string()
    response = make_response(file)
    response.headers["Content-Disposition"] = "attachment; filename=" + gala_id + "_entries.HY3"
    return response


@app.route('/entries/<gala_id>')
@check_admin_login
def get_entries(gala_id):
    with Mongo(db_config) as db:
        entries = list(db.entries.find({"gala_id": gala_id, "club_id" : session["clubid"]}))
        gala = db.gala.find_one({'title': gala_id, "club.id" : session["clubid"],'deleted':False})
        swimmers = list(db.swimmers.find({"club_id" : session["clubid"]}))
    if gala:
        def get_swimmer(swimmers, id):
            for swimmer in swimmers:
                if swimmer["swimmer_id"] == id:
                    return swimmer
            return None

        heats = []
        for heat in gala["heats"]:
            heat_with_swimmers = heat.copy()
            heat_with_swimmers["swimmers"] = []
            for entry in entries:
                if heat in entry["heats"]:
                    swimmer = get_swimmer(swimmers, entry["swimmer_id"])
                    heat_with_swimmers["swimmers"].append(swimmer)
            heat_with_swimmers["id"] = int(heat_with_swimmers["id"])
            heats.append(heat_with_swimmers)
        return render_template("entries.html", gala=gala, heats=heats)
    return "Invalid Gala Id"


@app.route("/registration", methods=["POST", "GET"])
@check_admin_login
def registration():
    if request.method == "GET":
        return render_template("manualform.html")

    swimmer_id = request.form['swimmer_id']
    gala_id = request.form['gala_id']
    club_id = session["clubid"]
    invalid = {"value" : False, "message" : ""}

    with Mongo() as db:
        gala = db.gala.find_one({'title': gala_id, 'club.id': club_id, 'deleted': False})
        swimmer = db.swimmers.find_one({'swimmer_id': swimmer_id, 'club_id': club_id})

    if gala is None:
        invalid["value"] = True
        invalid["message"] += "Gala ID Not Found"

    if swimmer is None:
        invalid["value"] = True
        if not invalid["message"] == "":
            invalid["message"] += ", "
        invalid["message"] += "Swimmer ID Not Found"

    if invalid["value"]:
        return render_template("manualform.html", invalid=invalid, swimmer_id=swimmer_id, gala_id=gala_id)
    else:
        gala = filter_heats(gala, swimmer)
        return render_template("form.html", swimmer=swimmer, gala=gala)



@app.route("/galas", methods=["GET"])
@check_admin_login
def galas():
    with Mongo({}) as db:
        galas = list(db.gala.find({"club.id" : session["clubid"], 'deleted': False}))
    return render_template("galas.html", galas=galas)


@app.route("/delete/<gala>", methods=["GET"])
@check_admin_login
def delete_gala(gala):
    club = session['clubid']
    with Mongo(db_config) as db:
        db.gala.update_one({"title": gala,"club.id": club}, {'$set': {'deleted': True}})
    return redirect(url_for('menu'))


def filter_heats(gala, swimmer):
    filtered_gala = gala.copy()
    filtered_gala["heats"] = []
    for heat in gala["heats"]:
        if _is_eligible(gala["date"], heat, swimmer):
            filtered_gala["heats"].append(heat)
    return filtered_gala


def _is_eligible(gala_date, heat, swimmer):
    age = calculate_age(swimmer["dob"], gala_date)
    return (get_gender(heat) == swimmer['sex'] and
            age<= int(heat["maxage"]) and age>=int(heat["minage"]))


def get_gender(heat):
    gender = heat['gender']
    if gender is 'B':
        return 'M'
    elif gender is 'G' or gender is 'W':
        return 'F'
    return gender


def calculate_age(dob,gala_date):
    age = (gala_date - dob).days//constants.DAYS_IN_YEAR
    return age


class InvalidFileTypeException(Exception):
    pass


def create_app():
    return app


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
