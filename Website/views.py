from flask import *
from .functions import *

views = Blueprint('views', __name__)

@views.route('/info', methods = ['GET', 'POST'])
def protected_page_general():
    if not session['logged_in']:
        return redirect(url_for("auth.login"))
    my_cursor = current_app.mydb.cursor()

    if request.method == "POST":
        form = request.form
        the_button = form.get('submit_button')
        if the_button == 'id':
            ide = form.get('id')
            result = search_by_id(ide, my_cursor)
            if not result:
                session['id'] = ''
                return render_template('General_lookup.html', id_result = 'Glasses Not Found', attribute_result = session['attributes'])
            session['id'] = result
            return render_template('General_lookup.html', id_result = session['id'], attribute_result = session['attributes'])
        elif the_button == "attributes":
            LCYL, LSPH, LAxis, LADD = form.get("cyl_left"), form.get("sph_left"), form.get("axis_left"), form.get("add_left")
            RCYL, RSPH, RAxis, RADD = form.get("cyl_right"), form.get("sph_right"), form.get("axis_right"), form.get("add_right")
            bridge, gender = form.get("bridge size"), form.get("gender")
            glasses_desc = search_by_attributes(cursor = my_cursor, lcyl=LCYL, lsph=LSPH, laxis=LAxis, ladd=LADD, rsph=RSPH, rcyl=RCYL, raxis=RAxis, radd=RADD, bridge=bridge, gender=gender)
            if not glasses_desc:
                session['attributes'] = ''
                return render_template('General_lookup.html', attribute_result = 'Glasses Not Found', id_result = session['id'])
            session['attributes'] = glasses_desc
            return render_template('General_lookup.html', attribute_result = session['attributes'], id_result = session['id'])

    return render_template('General_lookup.html', attribute_result = session['attributes'], id_result = session['id'])

@views.route('/admin', methods = ['Get', 'POST'])
def protected_page_admin():
    if not session['logged_in']:
        return redirect(url_for("auth.login"))
    if session['privilege'] == 1:
        return redirect(url_for('views.protected_page_general'))
    session['id'] = ''
    session['attributes'] = ''
    my_cursor = current_app.mydb.cursor()

    if request.method == 'POST':
        value = request.form.get('submit_button')
        if value == 'id':
            id = request.form.get("id")
            val = delete_from_database(id, my_cursor)
            if val:
                current_app.mydb.commit()
                return render_template('Admin_page.html', result1 = 'SUCCESS')
            else:
                return render_template('Admin_page.html', result1 = 'ID NOT FOUND')

        elif value == "attributes":
            form = request.form
            LCYL, LSPH, LAxis, LADD = form.get("cyl_left"), form.get("sph_left"), form.get("axis_left"), form.get("add_left")
            RCYL, RSPH, RAxis, RADD = form.get("cyl_right"), form.get("sph_right"), form.get("axis_right"), form.get("add_right")
            bridge, gender, description = form.get("bridge size"), form.get("gender"), form.get("description")
            if LSPH and RSPH and bridge and gender:
                my_cursor.execute("SELECT MAX(id) From Frame")
                ide = my_cursor.fetchall()[0][0] + 1
                val = add_to_database(ids = ide, lsph = LSPH, lcyl = LCYL, laxis = LAxis, ladd = LADD, rcyl= RCYL, rsph= RSPH, raxis= RAxis, radd= RADD, bridge= bridge, gender = gender, description = description, cursor = my_cursor)
                if val:
                    current_app.mydb.commit()
                    return render_template('Admin_page.html', result2 = "SUCCESS: ID " + str(ide) + " ADDED")
                else:
                    return render_template('Admin_page.html', result2 = "INVALID INPUTS")
            else:
                return render_template('Admin_page.html', result2 = 'MISSING REQUIRED VALUES')

        elif value == "bulk":
            frame_csv = request.files.get("frame_csv_file")
            lens_csv = request.files.get("lens_csv_file")
            frame_reader = csv_to_list(frame_csv)
            lens_reader = csv_to_list(lens_csv)

            if 2 * len(frame_reader) - 1 == len(lens_reader):
                for i in range(1, len(frame_reader)):
                    if frame_reader[i][0] == lens_reader[2*i][0] and lens_reader[2*i][0] == lens_reader[2*i-1][0] and lens_reader[2*i-1][1].strip() == 'R' and lens_reader[2*i][1].strip() == 'L':
                        print('start')
                        val = add_to_database(ids = int(frame_reader[i][0]), bridge = frame_reader[i][1], gender= frame_reader[i][2], description= frame_reader[i][3], lsph = lens_reader[2*i][2], lcyl= lens_reader[2*i][3], laxis = lens_reader[2*i][4] , ladd = lens_reader[2*i][5], rsph = lens_reader[2*i - 1][2], rcyl= lens_reader[2*i-1][3], raxis= lens_reader[2*i-1][4],radd= lens_reader[2*i-1][5], cursor = my_cursor)
                        if not val:
                            return render_template('Admin_page.html', result_3 ="INVALID INPUTS AT ROW " + str(i))
                    else:
                        return render_template('Admin_page.html', result_3="MISMATCH AT ROW " + str(i))
                current_app.mydb.commit()
                return render_template('Admin_page.html', result_3 = "SUCCESS")
            else:
                return render_template('Admin_page.html', result_3 = "FAILURE")

    return render_template('Admin_page.html')