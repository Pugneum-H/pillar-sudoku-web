from flask import *
from pillar_sudoku.pillar_sudoku import *




app = Flask(__name__)
app.secret_key = "" # nuh uh


app.config["DEBUG"] = True

def gen(fill_charset, width, height, ratio):
        sudoku = Sudoku([width, height], fill_charset[:width*height], (width*height)**2, grid=session["grid"])
        sudoku.generate()
        sudoku.remove(ratio)
        session["orig"].clear(); session['grid'].clear()
        session["orig"] = [i.strip(" ") for i in sudoku.get_grid()]
        session['grid'] = [i.strip(" ") for i in sudoku.get_grid()]
        return session['grid'], session['orig'], sudoku


def chars_filter(string, charset, len : int):
    return "".join([c for c in string if c in session['fill_charset']])[:len]


@app.route("/", methods=['GET', 'POST'])
def main():
    if not 'init'  in session:
        print("S"*1000)
        session['orig'] = []
        session['grid'] = []
        session['width'] = 3
        session['height'] = 3
        session['fill_charset'] = "123456789ABCDEFG"
        session['ratio'] = 0.5
        sudoku = Sudoku([session['width'],session['height']], session['fill_charset'][:session['width']*session['height']], (session['width']*session['height'])**2)
        sudoku = gen(session['fill_charset'], session['width'], session['height'], session['ratio'])[2]
        while not sudoku.check()[0] == True:
            sudoku = gen(session['fill_charset'], session['width'], session['height'], session['ratio'])[2]
        session['grid'].clear(); session['orig'].clear()
        session['grid'] = sudoku.get_grid()
        session["orig"] = sudoku.get_grid()
        session["init"] = True

    if request.method == 'POST':
        if "new" in request.form:
            try: session['width'], session['height'], session['ratio'] = int(list(request.form["sizes"])[0]), int(list(request.form["sizes"])[1]), float(request.form["difficulties"])
            except: pass
            sudoku = gen(session['fill_charset'], session['width'], session['height'], session['ratio'])[2]
            while not sudoku.check()[0] == True:
                sudoku = gen(session['fill_charset'], session['width'], session['height'], session['ratio'])[2]
            session['grid'].clear(); session['orig'].clear()
            session['grid'] = sudoku.get_grid()
            session['orig'] = sudoku.get_grid()
        else:
            print([session['width'], session['height']], session["fill_charset"][:session["width"]*session["height"]], (session["width"]*session["height"])**2, session["grid"])
            sudoku = Sudoku([session['width'], session['height']], session["fill_charset"][:session["width"]*session["height"]], (session["width"]*session["height"])**2, grid=session["grid"])
            session['orig'] = session['orig'].copy()
            session["grid"].clear()
            sudoku.set_grid([""*(session['width']*session['height'])**2])
            sudoku.set_grid([chars_filter(i, session['fill_charset'], 1)+" "*(1-len(i)) for i in request.values.getlist("fields")])

            session['grid'] = sudoku.get_grid()

    sudoku = Sudoku([session['width'], session['height']], session["fill_charset"][:session["width"]*session["height"]], (session["width"]*session["height"])**2, grid=session["grid"])

    if request.method == 'GET':
        pass

    session['complete'] = sudoku.check()[1]
    session['correct'] = sudoku.check()[0]


    return render_template('main.html', grid=sudoku.get_grid(), orig=session['orig'], width=session['width'], height=session['height'],
                           fill_charset=session['fill_charset'][:session['width']*session['height']], correct=session['correct'], complete=session['complete'],
                           size_selected=str(session['width'])+str(session['height']), difficulty_selected=str(session['ratio']))

@app.route("/info")
def info():
    return render_template("info.html")


if __name__ == "__main__":
    app.run(threaded = True, debug=True)
