from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from config import config

app = Flask(__name__)
app.config.from_object(config['development'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Usuario1(db.Model):
    __tablename__ = "site1_users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    nome_completo = db.Column(db.String(120), nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)

    def __repr__(self):
        return '<Usuario %r>' % self.nome_completo

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario1

class CardSite1(db.Model):
    __tablename__ = 'cards_site1'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('site1_users.id'), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)
    expiration_date = db.Column(db.String(10), nullable=False)
    cvv = db.Column(db.Integer, nullable=False)

class CardCschema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model= CardSite1
        include_fk = True



# Rota para listar todos os usuários
@app.route('/usuarios')
def listar_usuarios():
    usuarios = Usuario1.query.all()
    return UsuarioSchema(many=True).jsonify(usuarios)

# Rota para listar um usuário específico pelo ID
@app.route('/usuarios/<int:id>')
def listar_usuario(id):
    usuario = Usuario1.query.get(id)
    return UsuarioSchema().jsonify(usuario)

# Rota para inserir um novo usuário
@app.route('/usuarios/', methods=['POST'])
def inserir_usuario():
    usuario_schema = UsuarioSchema()
    usuario_data = request.get_json()
    usuario = Usuario1(**usuario_data)
    db.session.add(usuario)
    db.session.commit()
    return usuario_schema.jsonify(usuario)

# Rota para atualizar um usuário existente
@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    usuario_schema = UsuarioSchema()
    usuario = Usuario1.query.get(id)
    usuario = usuario_schema.load(request.json, instance=usuario)
    db.session.commit()
    return usuario_schema.jsonify(usuario)

# Rota para excluir um usuário existente
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    usuario = Usuario1.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário excluído com sucesso!'})



## cartão
@app.route('/cards/<int:user_id>', methods=['POST'])
def inserir_card(user_id):
    usuario = Usuario1.query.get_or_404(user_id)
    card_schema = CardCschema()
    card = card_schema.load(request.json)
    card.user = usuario
    db.session.add(card)
    db.session.commit()
    return card_schema.jsonify(card)

@app.route('/cards', methods=['GET'])
def listar_cards():
    user_id = request.args.get('user_id')
    usuario = Usuario1.query.get_or_404(user_id)
    cards = CardSite1.query.filter_by(user_id=user_id).all()
    card_schema = CardCschema(many=True)
    return card_schema.jsonify(cards)

@app.route('/cards/<int:card_id>', methods=['PUT'])
def atualizar_card(card_id):
    card_schema = CardCschema()
    card = CardSite1.query.get_or_404(card_id)
    card = card_schema.load(request.json, instance=card)
    db.session.commit()
    return card_schema.jsonify(card)

@app.route('/cards/<int:card_id>', methods=['DELETE'])
def excluir_card(card_id):
    card = CardSite1.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()
    return jsonify({'mensagem': 'Cartão excluído com sucesso!'})

@app.errorhandler(404)
def nao_encontrado(e):
    return jsonify({'mensagem': 'Recurso não encontrado'}), 404

# Execução do aplicativo
if __name__ == '__main__':
    app.run(debug=True)
