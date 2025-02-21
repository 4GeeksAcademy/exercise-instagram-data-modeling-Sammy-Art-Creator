import os
import sys
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Enum
from datetime import datetime
from eralchemy2 import render_er

# Crear la base para definir los modelos
Base = declarative_base()

# Definición de la tabla User (Usuarios)
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)  # Identificador único del usuario
    username = Column(String, unique=True, nullable=False)  # Nombre de usuario único
    firstname = Column(String, nullable=False)  # Nombre del usuario
    lastname = Column(String, nullable=False)  # Apellido del usuario
    email = Column(String, unique=True, nullable=False)  # Correo electrónico único

    posts = relationship('Post', backref='user')  # Relación con la tabla Post (un usuario puede tener varios posts)
    comments = relationship('Comment', backref='author')  # Relación con la tabla Comment (un usuario puede hacer varios comentarios)

# Definición de la tabla Post (Publicaciones)
class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)  # Identificador único de la publicación
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)  # Relación con el usuario que creó el post
    
    media = relationship('Media', backref='post')  # Relación con la tabla Media (un post puede tener varias imágenes/videos)

# Definición de la tabla Media (Imágenes/Videos)
class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)  # Identificador único del medio
    type = Column(Enum('image', 'video', name='media_type'), nullable=False)  # Tipo de medio (imagen/video)
    url = Column(String, nullable=False)  # URL donde se almacena la imagen o video
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)  # Relación con la publicación a la que pertenece
    
# Definición de la tabla Comment (Comentarios)
class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)  # Identificador único del comentario
    comment_text = Column(String, nullable=False)  # Contenido del comentario
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)  # Relación con el usuario que hizo el comentario
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)  # Relación con el post comentado
    
    post = relationship('Post', backref='comments')  # Relación con la tabla Post

# Definición de la tabla Follower (Seguidores)
class Follower(Base):
    __tablename__ = 'follower'
    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)  # Usuario que sigue a otro
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)  # Usuario que está siendo seguido

# Generación del diagrama de la base de datos
try:
    result = render_er(Base, 'diagram.png')  # Genera el diagrama de la base de datos y lo guarda como diagram.png
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
