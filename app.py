from flask import Flask, render_template, request, redirect, send_file, url_for, session
import json
import datetime
import sqlite3
puples = ['Иванов', 'Петров', 'Сидоров']
count = 0
mydb = sqlite3.connect('base.sqlite')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string' 
login = 0
password = 0



@app.route('/', methods=['POST', 'GET'])
def index():
    session['visit'] = 0
    global login
    global count
    global password
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        
        mydb = sqlite3.connect('base.sqlite')
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM organization_info')
        myresult = mycursor.fetchall()
        for row in myresult:
            if login == row[0] and password == row[1]:
                session['visit'] = 1
                print(session['visit'])
                return render_template('index.html', vis=session['visit'], login=login)
        session['visit'] = 0
        return render_template('404error.html')
    else:
        return render_template('index.html', vis=session['visit'])


@app.route('/add_puple', methods=['POST', 'GET'])
def add_tema():
    if request.method == 'POST':
        try:
            fio = request.form['fio']
            print(fio)
            surname = fio.split(' ')[0]
            name = fio.split(' ')[1]
            patronymic = fio.split(' ')[2]
            class_puple = request.form['class_puple']
            age = request.form['age']

            mydb = sqlite3.connect('base.sqlite')
            mycursor = mydb.cursor()
        
            sqlFormula = "INSERT INTO puples_info (name, surname, patronymic, class, age, c_first, c_second, c_third) VALUES (?,?,?,?,?,?,?,?)"
            mycursor.execute(sqlFormula, (name, surname, patronymic, int(class_puple), int(age), 0, 0, 0))
            mydb.commit()

            try:
                return render_template('index.html')
            except:
                return 'При добавлении ученика произошла ошибка'
        except:
            return 'При добавлении ученика произошла ошибка'
    else:
        return render_template('add_puple.html')
        




def exit_acc():
    session['visit'] = 0
    print('wdwdwdw')

@app.route('/add_achieve', methods=['POST', 'GET'])
def add_achieve():
    if request.method == 'POST':
        date = request.form['date']
        puple_fio = request.form['puple']
        surname = puple_fio.split(' ')[0]
        name = puple_fio.split(' ')[1]
        patronymic = puple_fio.split(' ')[2]
        win_place = request.form['win_place']
        description = request.form['description']
        f = request.files['file']
        f.save(f'static/img/{f.filename}')
        achieve_png_link = f'static/img/{f.filename}'

        mydb = sqlite3.connect('base.sqlite')
        mycursor = mydb.cursor()
        


        mydb = sqlite3.connect('base.sqlite')
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT (id) FROM puples_info WHERE name='{name}' AND surname='{surname}' AND patronymic='{patronymic}'")
        myresult = mycursor.fetchall()
        print(len(myresult))
        sqlFormula = "INSERT INTO achievements_puples (id_puple, ocup_place, description, 'date', link_png) VALUES (?,?,?,?,?)"
        mycursor.execute(sqlFormula, (myresult[0][0], int(win_place), description, date, achieve_png_link))
        mydb.commit()
        print('Прошло')
        return render_template('index.html')
            
    else:
        mydb = sqlite3.connect('base.sqlite')
        mycursor = mydb.cursor()
        puples = []
        mycursor.execute("SELECT * FROM puples_info")
        myresult = mycursor.fetchall()
        for row in myresult:
            puples.append(f'{row[2]} {row[1]} {row[3]}')
        return render_template('add_achieve.html', puples=puples)

        

@app.route('/info_puple', methods=['POST', 'GET'])
def info_puple():
    if request.method == 'POST':
        fio = request.form['puple']
        name = fio.split(' ')[1]
        surname = fio.split(' ')[0]
        patronymic = fio.split(' ')[2]
        mydb = sqlite3.connect('base.sqlite')           # НАХОЖУ ДОСТИЖЕНИЯ
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT (id) FROM puples_info WHERE name='{name}' AND surname='{surname}' AND patronymic='{patronymic}'")
        myresult = mycursor.fetchall()
        id_ = myresult[0][0]
        mycursor.execute(f"SELECT * FROM achievements_puples WHERE id_puple='{id_}'")
        my_achievs = mycursor.fetchall()
        print(my_achievs)
        return render_template('list_achievement.html', my_achievs=my_achievs)
    else:
        mydb = sqlite3.connect('base.sqlite')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM puples_info")
        myresult = mycursor.fetchall()
        puples = []
        for row in myresult:
            puples.append(f'{row[2]} {row[1]} {row[3]}')
        return render_template('info_puple.html', puples=puples)




@app.route('/all', methods=['POST', 'GET'])
def all_rait():
    mydb = sqlite3.connect('base.sqlite')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM puples_info")
    myresult = mycursor.fetchall()
    itogs = {}
    puples = []
    for row in myresult:
        itogs[f'{row[2]} {row[1]} {row[3]}'] = [row[6], row[7], row[8]] 
        puples.append(f'{row[2]} {row[1]} {row[3]}')
    dates = ['кол-во 1-ых мест', 'кол-во 2-ых мест', 'кол-во 3-ых мест']
    ocenki = {}
        
            # a = 0
            # for row in ocenki[name]:
            #     if row != 'itog' and 'н' not in ocenki[name][row] and 'б' not in ocenki[name][row]:
            #         ocenki[name]['itog'] += int(ocenki[name][row])
            #         a += 1
            # if a != 0:
            #     ocenki[name]['itog'] = ocenki[name]['itog'] // a
            # itogs.append(ocenki[name]['itog'])
      #  with open('static/graffik.json', 'w') as file:
       #     json.dump(itogs, file, indent=2, ensure_ascii=False)
    return render_template('jurnal_table.html', dates=dates, puples=puples, itogs=itogs)
    # else:
    #     return render_template('404error.html')







if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=7000)
