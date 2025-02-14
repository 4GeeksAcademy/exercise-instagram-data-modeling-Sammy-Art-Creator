import os
import sys
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
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
    email = Column(String, unique=True, nullable=False)  # Correo electrónico único
    firstname = Column(String, nullable=False)  # Nombre del usuario
    lastname = Column(String, nullable=False)  # Apellido del usuario
    password = Column(String, nullable=False)  # Contraseña
    created_at = Column(DateTime, default=datetime.utcnow)  # Fecha de creación del usuario
    
    posts = relationship('Post', back_populates='user')  # Relación con la tabla Post (un usuario puede tener varios posts)
    comments = relationship('Comment', back_populates='author')  # Relación con la tabla Comment (un usuario puede hacer varios comentarios)

# Definición de la tabla Post (Publicaciones)
class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)  # Identificador único de la publicación
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)  # Relación con el usuario que creó el post
    caption = Column(String, nullable=True)  # Texto de la publicación
    created_at = Column(DateTime, default=datetime.utcnow)  # Fecha de creación del post
    
    user = relationship('User', back_populates='posts')  # Relación con la tabla User
    media = relationship('Media', back_populates='post')  # Relación con la tabla Media (un post puede tener varias imágenes/videos)
    comments = relationship('Comment', back_populates='post')  # Relación con la tabla Comment (un post puede tener varios comentarios)

# Definición de la tabla Media (Imágenes/Videos)
class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)  # Identificador único del medio
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)  # Relación con la publicación a la que pertenece
    type = Column(Enum('image', 'video', name='media_type'), nullable=False)  # Tipo de medio (imagen/video)
    url = Column(String, nullable=False)  # URL donde se almacena la imagen o video
    
    post = relationship('Post', back_populates='media')  # Relación con la tabla Post

# Definición de la tabla Comment (Comentarios)
class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)  # Identificador único del comentario
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)  # Relación con el post comentado
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)  # Relación con el usuario que hizo el comentario
    comment_text = Column(String, nullable=False)  # Contenido del comentario
    created_at = Column(DateTime, default=datetime.utcnow)  # Fecha de creación del comentario
    
    post = relationship('Post', back_populates='comments')  # Relación con la tabla Post
    author = relationship('User', back_populates='comments')  # Relación con la tabla User

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
