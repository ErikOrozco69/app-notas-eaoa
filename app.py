from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://wypksmatdmjrec:24f9898d444d48ce03d9e19efad4c6707c7772b354d56a25f5d7bb2f5edbba83@ec2-52-86-193-24.compute-1.amazonaws.com:5432/dee2mqi73so5dn'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False



class Notas(db.Model):
    '''Clase Notas'''
    __tablename__="notas"
    idNota=db.Column(db.Integer,primary_key =True)
    tituloNota=db.Column(db.String(80))
    cuerpoNota=db.Column(db.String(150))

    def __init__(self,idNota,tituloNota, cuerpoNota):
        self.tituloNota=tituloNota
        self.cuerpoNota =cuerpoNota



@app.route('/')
def index():
    objeto={"nombre":"Erik",
          "apellido":"Orozco"
          }
    nombre="ERIK"
    lista_nombres=["ESMERALDA","JUAN","DAVID"]
    print("Hola mundo")
    return render_template("index.html",variable =lista_nombres)


@app.route("/about")
def about():
    return "Estas en la vista about"

@app.route("/crearnota", methods =['POST'])
def crearnota():
    campotitulo=request.form["campotitulo"]
    campocuerpo=request.form["campocuerpo"]
    print(campotitulo)
    print(campocuerpo)
    notaNueva =Notas(idNota=1,tituloNota=campotitulo,cuerpoNota=campocuerpo)
    db.session.add(notaNueva)
    db.session.commit()

    return render_template("index.html",tituloNota=campotitulo,cuerpoNota=campocuerpo)
    #return"nota creada" + campotitulo + campocuerpo


@app.route("/leernotas")
def leernotas():
    consulta_notas=Notas.query.all()
    print(consulta_notas)
    for nota in consulta_notas:
        titulo =nota.tituloNota
        cuerpo=nota.cuerpoNota
        print(nota.tituloNota)
        print(nota.cuerpoNota)
        
    return render_template("index.html",consulta=consulta_notas)


@app.route("/eliminarnota/<id>")
def eliminar(id):
    nota=Notas.query.filter_by(idNota=int(id)).delete()
    print(nota)
    db.session.commit()
    return redirect("/leernotas")


@app.route("/editarnota/<id>")
def editar(id):
    nota=Notas.query.filter_by(idNota=int(id)).first()
    print(nota)
    print(nota.tituloNota)
    print(nota.cuerpoNota)
    return render_template("/modificaNota.html",nota = nota)

@app.route("/modificarnota",methods=['POST'])
def modificarnota():
    idnota =request.form['idnota']
    nuevo_titulo =request.form['campotitulo']
    nuevo_cuerpo =request.form['campocuerpo']
    nota =Notas.query.filter_by(idNota =int(idnota)).first()
    nota.tituloNota =nuevo_titulo
    nota.cuerpoNota =nuevo_cuerpo
    db.session.commit()
    return redirect("/leernotas")


if __name__ =="__main__":
    db.create_all()
    app.run()