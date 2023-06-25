from comunidadeblog import app, database
from comunidadeblog.models import Usuario

# Criando banco de dados automaticamente ele cria uma pasta chamada instance e salva o db
# with app.app_context():
#     database.create_all()

with app.app_context():
    database.drop_all()     # Deleta tudo que tem no banco
    database.create_all()

# with app.app_context():
#     usuario = Usuario.query.filter_by(username='Wallace').first()
#     print(usuario.senha)

# Incluindo dados no banco de dados
# with app.app_context():
#     usuario = Usuario(username='Michele', email='michele@gmail.com', senha='123456')
#     usuario2 = Usuario(username='Wallace', email='wallace@uol.com', senha='123456')
#
#     # Incluindo dados no banco de dados
#     database.session.add(usuario)
#     database.session.add(usuario2)
#
#     database.session.commit()

# Consultando informações no banco de dados
# with app.app_context():
#     meus_usuarios = Usuario.query.all()
#     print(meus_usuarios)
#     primeiro_usuario = meus_usuarios[0]
#     print(primeiro_usuario)
#
#     #ou
#     prim_user = Usuario.query.first()
#     print(prim_user)
#
#     # Pegando informações de cada usuário
#     print(prim_user.id)
#     print(prim_user.username)
#
#
#     filtro_especifico = Usuario.query.filter_by(username='Wallace').first()
#     print(filtro_especifico.email)



# with app.app_context():
#     # Inserindo valores na tabela Post
#     # post = Post(titulo='Meu primeiro Post', corpo='Corto do primeiro Post', id_usuario=1)
#     # database.session.add(post)
#     # database.session.commit()
#
#     consultando_post_banco = Post.query.all()
#     for item in consultando_post_banco:
#         print(item.titulo)
#         print(item.corpo)
#         print(item.id_usuario)
#
#         # Pegando informação da tabela usuário que possui relacionamento com a tabela Post
#         print(item.autor.email)


