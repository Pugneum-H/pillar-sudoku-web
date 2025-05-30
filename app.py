from flask import *
from pillar_sudoku.pillar_sudoku import *
# from flask_wtf.csrf import CSRFProtect
# from flask_talisman import Talisman




app = Flask(__name__)



# Talisman(app)
# csrf = CSRFProtect(app)

orig = []
grid = []
width = 3
height = 3
fill_charset = "123456789ABCDEFG"
ratio = 0.5
sudoku = Sudoku([width,height], fill_charset[:width*height], (width*height)**2)

def gen(fill_charset, width, height, ratio):
    global grid, orig, sudoku, out
    sudoku = Sudoku([width, height], fill_charset[:width*height], (width*height)**2)
    sudoku.generate()
    sudoku.remove(ratio)
    orig.clear(); grid.clear()
    grid = [i.strip(" ") for i in sudoku.get_grid()]
    orig = [i.strip(" ") for i in sudoku.get_grid()]
    return grid, orig


def chars_filter(string, charset, len : int):
    return "".join([c for c in string if c in fill_charset])[:len]

gen(fill_charset, width, height, ratio)
while not sudoku.check()[0] == True:
    gen(fill_charset, width, height, ratio)
grid.clear(); orig.clear()
grid = sudoku.get_grid()
orig = sudoku.get_grid()

@app.route("/", methods=['GET', 'POST'])
def main():
    global grid, orig, width, height, fill_charset, sudoku, ratio, out
    if request.method == 'POST':
        if "new" in request.form:
            try: width, height, ratio = int(list(request.form["sizes"])[0]), int(list(request.form["sizes"])[1]), float(request.form["difficulties"])
            except: pass
            gen(fill_charset, width, height, ratio)
            while not sudoku.check()[0] == True:
                gen(fill_charset, width, height, ratio)
            grid.clear(); orig.clear()
            grid = sudoku.get_grid()
            orig = sudoku.get_grid()
        else:
            orig = orig.copy()
            grid.clear()
            sudoku.set_grid([""*(width*height)**2])
            sudoku.set_grid([chars_filter(i, fill_charset, 1)+" "*(1-len(i)) for i in request.values.getlist("fields")])

            grid = sudoku.get_grid()



    if request.method == 'GET':
        pass
    complete = sudoku.check()[1]
    correct = sudoku.check()[0]


    return render_template('main.html', grid=sudoku.get_grid(), orig=orig, width=width, height=height,
                           fill_charset=fill_charset[:width*height], correct=correct, complete=complete,
                           size_selected=str(width)+str(height), difficulty_selected=str(ratio))

@app.route("/info")
def info():
    return render_template("info.html")



