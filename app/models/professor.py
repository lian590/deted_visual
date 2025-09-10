from .. import db

class Professor(db.Model):
    __tablename__ = 'professores'

    id = db.Column(db.Integer, primary_key=True)
    # Adicione outros campos conforme necessário
    nome = db.Column(db.String(100))
    # etc.

    def __repr__(self):
        return f'<Professor {self.nome}>'
