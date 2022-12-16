from flask import Flask, render_template, request, redirect, url_for, flash,send_file
#from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import check_password_hash,generate_password_hash

#from config import config

from math import fabs
#from flask_mysqldb import MySQL
from pathlib import Path
import sys, os, glob
from PyPDF2 import PdfFileWriter, PdfFileReader

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from shutil import rmtree
#import for concatenate pdf files
from PyPDF2 import PdfFileMerger

# importaciones para la animación del proceso
import itertools
import threading
import time

# import for convert numbers to words
from num2words import num2words

#import for concatenate pdf files
from PyPDF2 import PdfFileMerger
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from pathlib import Path
from PyPDF2 import PdfFileWriter, PdfFileReader



# Models:
#from models.ModelUser import ModelUser

# Entities:
#from models.entities.User import User

app = Flask(__name__)
csrf = CSRFProtect()
#db = MySQL(app)
login_manager_app = LoginManager(app)
# settings
app.secret_key = "mysecretkey"
output_path = ""
test = ""
UPLOAD_FOLDER = 'pdf_orig'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'pdf_orig' # carpeta de origen
ALLOWED_EXTENSIONS = set(['PDF', 'pdf'])
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


#----------------------------------------------------------------------------------------------------------------------
#------------FUNCIONES DEL FOLIADOR DE PDF'S--------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------

def folders_create(numb_path, source_path):
    # create path for PDF documents
    if not os.path.isdir(numb_path):
        os.makedirs(numb_path)
    # create path for PDF documents for concatening operations
    if not os.path.isdir(source_path):
        os.makedirs(source_path)

def clear_screen():
    if sys.platform == "win32":
        os.system('cls')
    if sys.platform == "linux1" or sys.platform == "linux2":
        os.system('clear')

def concatenar(numb_path, source_path):
    pdf_concatenado = (Path.cwd() / numb_path / "tmp_concatenado.pdf")

    # lista del contenido de la carpeta
    print("Concatenando archivos")
    for path in source_path.glob("*.pdf"):
        print("     " + path.name)

    # ordenar los files por nombre
    pdf_list = list(source_path.glob("*.pdf"))  # crear lista de archivos PDF
    pdf_list.sort()  # ordenarlos alfabeticamente

    # instanciar clase "PdfFileMerger"
    pdf_merger = PdfFileMerger()

    # Now loop over the paths in the sorted expense_reports list and append them to pdf_merger:
    for path in pdf_list:
        pdf_merger.append(str(path))

    with Path(pdf_concatenado).open(mode="wb") as output_file:
        pdf_merger.write(output_file)

    return pdf_concatenado

def createPagePdf(caps, pdf_path, num_from, num_ini, num, tmp, num_opc, font_name, font_size, position, left_margin, right_margin,num_opc2):
    c = canvas.Canvas(tmp)
    # print(num_ini+num)
    # margins left and right
    chars_lm = " " * left_margin
    chars_rm = " " * right_margin
    palabras = numeracion = numeracion2 = ""

    if num_ini == -1:
        pgn = num
    else:
        pgn = num_ini # page number

    input1 = PdfFileReader(open(pdf_path,'rb')) # for finding page dimensions

    # iniciar operaciones
    for i in range(1, num+1):
        if i >= num_from:
            c.setFont(font_name, font_size)  # establish font

            # find dimensions of the page, para getPage el primer número de página es Cero, por eso uso "i-1"
            p_width = float(input1.getPage(i-1).mediaBox.getWidth()) # en puntos de computadora
            p_height = float(input1.getPage(i-1).mediaBox.getHeight()) # en puntos de computadora

            max_top = round(p_height / 2.8346438836889,0) # convertir a mm
            max_right = round( p_width / 2.8346438836889,0) # convertir a mm

            # posiciones
            if position == '1':
                x = 4
                y1 = max_top - 8
                y2 = y1 - 4
            if position == '2':
                x = max_right // 2
                y1 = max_top - 8
                y2 = y1 - 4
            if position == '3':
                x = max_right - 4
                y1 = max_top - 8
                y2 = y1 - 4
            if position == '4':
                x = 4
                y1 = 4
                if num_opc2 != "e":
                    y1 = 8
                y2 = 4
            if position == '5':
                x = max_right // 2
                y1 = 4
                if num_opc2 != "e":
                    y1 = 8
                y2 = 4
            if position == '6':
                x = max_right - 4
                y1 = 4  # el mínimo es 0 pero sale al borde de la hoja
                if num_opc2 != "e":
                    y1 = 8
                y2 = 4



            if num_opc in ('b', 'c', 'd') or num_opc2 in ('b', 'c', 'd'):
                palabras = num2words(pgn, to='cardinal', lang='es').capitalize()
                if caps == 2:
                    palabras = palabras.upper()

            # Line 1: number expressed in words
            if num_opc == 'a': # only numbers
                numeracion = chars_lm + str(pgn) + chars_rm
            if num_opc == 'b': # numbers + words
                numeracion = chars_lm + str(pgn) + " " + palabras + chars_rm
            if num_opc == 'c': # words + numbers
                numeracion = chars_lm + palabras + " " + str(pgn) + chars_rm
            if num_opc == 'd':  # only words
                numeracion = chars_lm + palabras + chars_rm

            # Line 2: number expressed in words
            if num_opc2 == 'a': # only numbers
                numeracion2 = chars_lm + str(pgn) + chars_rm
            if num_opc2 == 'b': # numbers + words
                numeracion2 = chars_lm + str(pgn) + " " + palabras + chars_rm
            if num_opc2 == 'c': # words + numbers
                numeracion2 = chars_lm + palabras + " " + str(pgn) + chars_rm
            if num_opc2 == 'd':  # only words
                numeracion2 = chars_lm + palabras + chars_rm
            if num_opc2 == 'e':  # nothing
                numeracion2 = ""

            # escribir num pag
            if position in ('1','4'):
                c.drawString(x * mm, y1 * mm, numeracion)
                if num_opc2 != "e":
                    c.drawString(x * mm, y2 * mm, numeracion2)

            if position in ('2','5'):
                c.drawCentredString(x * mm, y1 * mm, numeracion)
                if num_opc2 != "e":
                    c.drawCentredString(x * mm, y2 * mm, numeracion2)

            if position in ('3','6'):
                c.drawRightString(x * mm, y1 * mm, numeracion)
                if num_opc2 != "e":
                    c.drawRightString(x * mm, y2 * mm, numeracion2)

            if num_ini == -1:
                pgn -= 1
            else:
                pgn += 1 # increase page number


        c.showPage()
    c.save()
    return
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#------------RUTAS DE TRABAJO--------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
@app.route('/foliador')
#@login_required
def foliador():
    return render_template('foliador.html')

@app.route('/foliador/useFoliador', methods=['POST'])
#@login_required
def useFoliador():
    flash("INCIO")
    if request.method == 'POST':
        def animate():
            for c in itertools.cycle(['|', '/', '-', '\\']):
                if work_done:
                    break
                sys.stdout.write('\rProcesando ' + c)
                sys.stdout.flush()
                time.sleep(0.1)
            sys.stdout.write('\r¡Hecho!')
        customRadioInline1 = request.form['num_opc']
        #flash(customRadioInline1)
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File(s) successfully uploaded')
        
        #LINEA 1 
        num_opc = request.form['num_opc']
        if len(num_opc) == 0:
            num_opc = 'a'
        if num_opc not in ("a","b","c","d"):
            flash("Escoja una de las opciones: a,b,c,d")
        #LINEA 2
        num_opc2 = request.form['num_opc2']    
        if len(num_opc2) == 0:
            num_opc2 = 'e'
        if num_opc2 not in ("a","b","c","d","e"):
            flash("Escoja una de las opciones: a,b,c,d,e")
        #TIPO DE LETRA
        font_name = request.form['font_name']    
        if font_name == "":
            font_name = "a"#POR DEFECTO

        if font_name == "a":
            font_name = "Courier"
        if font_name == "b":
            font_name = "Courier-Bold"
        if font_name == "c":
            font_name = "Courier-BoldOblique"
        if font_name == "d":
            font_name = "Courier-Oblique"

        if font_name == "e":
            font_name = "Helvetica"
        if font_name == "f":
            font_name = "Helvetica-Bold"
        if font_name == "g":
            font_name = "Helvetica-BoldOblique"
        if font_name == "h":
            font_name = "Helvetica-Oblique"

        if font_name == "i":
            font_name = "Symbol"

        if font_name == "j":
            font_name = "Times-Bold"
        if font_name == "k":
            font_name = "Times-BoldItalic"
        if font_name == "l":
            font_name = "Times-Italic"
        if font_name == "m":
            font_name = "Times-Roman"

        #Tamaño de letra
        font_size = request.form['font_size'] 
        if font_size == "":
            font_size = 10
        else:
            font_size = int(font_size)

        #Margen Izquierdo
        left_margin = request.form['left_margin'] 
        if left_margin == "":
            left_margin = 0
        else:
            left_margin = int(left_margin)

        #Margen Derecho
        right_margin = request.form['right_margin'] 
        if right_margin == "":
            right_margin = 0
        else:
            right_margin = int(right_margin)

        #MAYUSCULA O MINUSCULa  
        caps = request.form['caps']
        if caps == "1":
            caps = 1
        else:
            caps = 2

        #Posicion de la Numeracion
        position = request.form['position'] 
        if position == "":
            position = '5'
        if position not in ('1','2','3','4','5','6'):
            position = '5'

        #Numero Inicial
        num_ini_x = request.form['num_ini_x'] 
        if num_ini_x.strip() == "":
            num_ini = 1
        else:
            num_ini = int(num_ini_x)

        #Numerar desde la página (1) 
        num_from_x = request.form['num_from_x'] 
        if num_from_x.strip() == "":
            num_from = 1
        else:
            num_from = int(num_from_x)

        #
        numb_path = (Path.cwd() / "pdf_num")
        source_path = (Path.cwd() / "pdf_orig")

        #folders_create(numb_path, source_path)

        pdf_list = glob.glob(str(source_path) + "\*.pdf")
        pdf_qty = len(pdf_list)
        if pdf_qty == 0: # pdf source files not included
            sys.exit("Guarde los archivos originales en {}".format(source_path))

        if pdf_qty > 1:  # if exists more then 1 pdf, then concatenate
            pdf_path = concatenar(numb_path, source_path)
        else: # if only one, use it
            pdf_path = Path(numb_path) / Path(pdf_list[0]) # path of the source file given by user
            flash(pdf_path)

        base = os.path.basename(pdf_path) # isolates only the file name and suffix
        tmp = "__tmp.pdf"

        batch = 0
        output = PdfFileWriter() # create output object, this is the origin of the PDF result file

        with open(str(pdf_path), 'rb') as f:
            pdf = PdfFileReader(f, strict=False)
            n = pdf.getNumPages()
            if batch == 0:
                batch = -n

            # -------- initialize animation ----------
            work_done = False
            t = threading.Thread(target=animate)
            t.start()
            # -----------------------------------------
            # method for create blank PDF with numerated pages. n= number of pages, tmp= filename
            createPagePdf(caps, pdf_path, num_from, num_ini, n, tmp, num_opc, font_name, font_size, position, left_margin, right_margin,num_opc2)
        
            with open(tmp, 'rb') as ftmp:
                numberPdf = PdfFileReader(ftmp) #obj from the blank numbered PDF file
                for p in range(n): # loops for the pages quantity
                    # print('page: %d of %d' % (p, n))
                    page = pdf.getPage(p) # obj that recovers page number 'p' from source PDF file
                    numberLayer = numberPdf.getPage(p) # obj that recovers page number 'p' from blank numbered PDF file

                    # print(numberLayer)
                    page.mergePage(numberLayer) # merges both pages number 'p'
                    output.addPage(page) # adds the page to the obj 'output'

                # save the result PDF file
                if output.getNumPages(): # if there are resulting pages, proceed
                    # create name of output file
                    name = pdf_path.stem 
                    if name == "tmp_concatenado":
                        name = "concatenado"

                    output_path = (numb_path / (name + "_numerado" + pdf_path.suffix))
                    with open(str(output_path), 'wb') as f:
                        output.write(f)

            os.remove(tmp) # borrar archivos temporales
            work_done = True # terminate animation
        # borrar archivo concatenado temporal si existiera
        if os.path.exists(Path.cwd() / numb_path / "tmp_concatenado.pdf"):
            os.remove(Path.cwd() / numb_path / "tmp_concatenado.pdf")    

        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        
        return send_file(output_path, as_attachment=False)
         
@app.route('/foliador/download',methods=['POST'])
#@login_required
def download():
    if request.method == 'POST':
        descargar = request.form['descargar']
        if(descargar == ""):
            flash("Primero suba un Documento")
            return render_template('foliador.html')                  
        else:            
            return send_file(descargar, as_attachment=True)

@app.route('/')
def Index():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS









#@login_manager_app.user_loader
#def load_user(id):
    #return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
#@login_required
def home():
    return render_template('home.html')


@app.route('/protected')
#@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    #app.config.from_object(config['development'])
    app.run(debug=True)
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
