from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

# Conexion a la Base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user2:Alexis165904841+@localhost:3306/dbpythonapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
mrshll = Marshmallow(app)


class Categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_nombre = db.Column(db.String(100))
    cat_descr = db.Column(db.String(100))

    def __init__(self, cat_nombre, cat_descr):
        self.cat_nombre = cat_nombre
        self.cat_descr = cat_descr


db.create_all()


class CategoriaSchema(mrshll.Schema):
    class Meta:
        fields = ('cat_id', 'cat_nombre', 'cat_descr')


# Una sola respuesta
categoria_schema = CategoriaSchema()

# Cuando sean muchas respuestas
categorias_schema = CategoriaSchema(many=True)

# GET todo


@app.route("/categorias", methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)

# GET por ID


@app.route("/categorias/<id>", methods=['GET'])
def get_categoria_por_id(id):
    una_cat = Categoria.query.get(id)
    return categoria_schema.jsonify(una_cat)

# POSt (insertar)


@app.route('/agregar', methods=['POST'])
def insertar():
    cat_nombre = request.json['cat_nombre']
    cat_descr = request.json['cat_descr']

    nuevo_registro = Categoria(cat_nombre=cat_nombre, cat_descr=cat_descr)
    db.session.add(nuevo_registro)
    db.session.commit()
    return categoria_schema.jsonify(nuevo_registro)


# Update
@app.route("/actualizar/<id>", methods=['PUT'])
def actualizar(id):
    id_cat = Categoria.query.get(id)
    data = request.get_json(force=True)
    cat_nombre = data['cat_nombre']
    cat_descr = data['cat_descr']

    id_cat.cat_nombre = cat_nombre
    id_cat.cat_descr = cat_descr

    db.session.commit()
    return categoria_schema.jsonify(id_cat)


# Delete (realmente no se debe eliminar un registro en produccion)
@app.route("/eliminar/<id>", methods=['DELETE'])
def eliminar(id):
    eliminar_cat = Categoria.query.get(id)
    db.session.delete(eliminar_cat)
    db.session.commit()
    return categoria_schema.jsonify(eliminar_cat)


@app.route("/", methods=['GET'])
def index():
    return jsonify({"mensaje": "Hola mundo"})


if __name__ == "__main__":
    app.run(debug=True)
