from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from functools import wraps
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='../templates')
app.secret_key = 'tu-clave-secreta-muy-segura'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Asegurar que el directorio de uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Ruta para servir archivos subidos
@app.route('/static/uploads/<filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Conexión a la base de datos
def get_db():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'recetas.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# Decorador para requerir login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Ruta principal - ver recetas por categorías
@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()

    # Obtener recetas por categoría
    def get_recetas_por_categoria(categoria_nombre):
        cursor.execute("""
            SELECT r.*, c.nombre as categoria,
                   CASE WHEN u.id = 1 THEN 'My Cooking' ELSE u.nombre_usuario END as autor,
                   u.id as autor_id,
                   COUNT(l.usuario_id) as likes_count
            FROM recetas r
            LEFT JOIN categorias c ON r.id_categoria = c.id
            LEFT JOIN usuarios u ON r.id_usuario = u.id
            LEFT JOIN likes l ON r.id = l.receta_id
            WHERE c.nombre = ?
            GROUP BY r.id
            ORDER BY r.id DESC
        """, (categoria_nombre,))
        return cursor.fetchall()

    # Obtener todas las recetas
    cursor.execute("""
        SELECT r.*, c.nombre as categoria,
                   CASE WHEN u.id = 1 THEN 'My Cooking' ELSE u.nombre_usuario END as autor,
                   u.id as autor_id,
               COUNT(l.usuario_id) as likes_count
        FROM recetas r
        LEFT JOIN categorias c ON r.id_categoria = c.id
        LEFT JOIN usuarios u ON r.id_usuario = u.id
        LEFT JOIN likes l ON r.id = l.receta_id
        GROUP BY r.id
        ORDER BY r.id DESC
    """)
    recetas_usuarios = cursor.fetchall()

    recetas_vegetariano = get_recetas_por_categoria('Vegetariano')
    recetas_keto = get_recetas_por_categoria('Keto')
    recetas_postre = get_recetas_por_categoria('Postres')
    recetas_desayuno = get_recetas_por_categoria('Desayunos')
    recetas_cenas = get_recetas_por_categoria('Cenas')
    recetas_saludables = get_recetas_por_categoria('Saludable')

    conn.close()

    return render_template('index.html',
                         recetas_vegetariano=recetas_vegetariano,
                         recetas_keto=recetas_keto,
                         recetas_postre=recetas_postre,
                         recetas_desayuno=recetas_desayuno,
                         recetas_cenas=recetas_cenas,
                         recetas_saludables=recetas_saludables,
                         recetas_usuarios=recetas_usuarios)

# Registro de usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre_usuario, email, password) VALUES (?, ?, ?)",
                (nombre_usuario, email, password_hash)
            )
            conn.commit()
            flash('Usuario registrado exitosamente. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('El email ya está registrado.', 'error')
        finally:
            conn.close()

    return render_template('registro.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario and check_password_hash(usuario['password'], password):
            session['user_id'] = usuario['id']
            session['nombre_usuario'] = usuario['nombre_usuario']
            flash(f'¡Bienvenido, {usuario["nombre_usuario"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email o contraseña incorrectos.', 'error')

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('index'))

# Crear nueva receta
@app.route('/receta/nueva', methods=['GET', 'POST'])
@login_required
def nueva_receta():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        ingredientes = request.form['ingredientes']
        pasos = request.form['pasos']
        tiempo = request.form['tiempo']
        porciones = request.form['porciones']
        id_categoria = request.form['id_categoria']
        id_usuario = session['user_id']

        # Manejar subida de imagen
        if 'imagen' not in request.files:
            flash('Debes subir una imagen para la receta.', 'error')
            return redirect(request.url)

        file = request.files['imagen']
        if file.filename == '':
            flash('Debes seleccionar una imagen.', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Añadir timestamp para evitar nombres duplicados
            import time
            unique_filename = f"{int(time.time())}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            imagen_path = unique_filename
        else:
            flash('Tipo de archivo no permitido. Solo PNG y JPG.', 'error')
            return redirect(request.url)

        cursor.execute("""
            INSERT INTO recetas (titulo, descripcion, ingredientes, pasos, tiempo, porciones, id_categoria, id_usuario, imagen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (titulo, descripcion, ingredientes, pasos, tiempo, porciones, id_categoria, id_usuario, imagen_path))
        conn.commit()
        conn.close()

        flash('Receta creada exitosamente.', 'success')
        return redirect(url_for('mis_recetas'))

    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    conn.close()

    return render_template('receta_form.html', categorias=categorias, receta=None)

# Editar receta
@app.route('/receta/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_receta(id):
    conn = get_db()
    cursor = conn.cursor()

    # Verificar que la receta pertenece al usuario
    cursor.execute("SELECT * FROM recetas WHERE id = ? AND id_usuario = ?", (id, session['user_id']))
    receta = cursor.fetchone()
    if not receta:
        flash('No tienes permiso para editar esta receta.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        ingredientes = request.form['ingredientes']
        pasos = request.form['pasos']
        tiempo = request.form['tiempo']
        porciones = request.form['porciones']
        id_categoria = request.form['id_categoria']

        # Manejar subida de nueva imagen o mantener la existente
        imagen_path = receta['imagen']  # Por defecto mantener la imagen actual
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename != '' and allowed_file(file.filename):
                # Eliminar imagen anterior
                if receta['imagen'] and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], receta['imagen'])):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], receta['imagen']))

                filename = secure_filename(file.filename)
                import time
                unique_filename = f"{int(time.time())}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                imagen_path = unique_filename

        cursor.execute("""
            UPDATE recetas SET titulo=?, descripcion=?, ingredientes=?, pasos=?, tiempo=?, porciones=?, id_categoria=?, imagen=?
            WHERE id=? AND id_usuario=?
        """, (titulo, descripcion, ingredientes, pasos, tiempo, porciones, id_categoria, imagen_path, id, session['user_id']))
        conn.commit()
        conn.close()

        flash('Receta actualizada exitosamente.', 'success')
        return redirect(url_for('mis_recetas'))

    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    conn.close()

    return render_template('receta_form.html', categorias=categorias, receta=receta)

# Eliminar receta
@app.route('/receta/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_receta(id):
    conn = get_db()
    cursor = conn.cursor()

    # Verificar que la receta pertenece al usuario
    cursor.execute("SELECT * FROM recetas WHERE id = ? AND id_usuario = ?", (id, session['user_id']))
    if not cursor.fetchone():
        flash('No tienes permiso para eliminar esta receta.', 'error')
        return redirect(url_for('index'))

    cursor.execute("DELETE FROM recetas WHERE id = ? AND id_usuario = ?", (id, session['user_id']))
    conn.commit()
    conn.close()

    flash('Receta eliminada exitosamente.', 'success')
    return redirect(url_for('mis_recetas'))

# Ver mis recetas
@app.route('/mis-recetas')
@login_required
def mis_recetas():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, c.nombre as categoria,
               COUNT(l.usuario_id) as likes_count
        FROM recetas r
        LEFT JOIN categorias c ON r.id_categoria = c.id
        LEFT JOIN likes l ON r.id = l.receta_id
        WHERE r.id_usuario = ?
        GROUP BY r.id
        ORDER BY r.id DESC
    """, (session['user_id'],))
    recetas = cursor.fetchall()
    conn.close()
    return render_template('mis_recetas.html', recetas=recetas)

# Ver detalle de receta
@app.route('/receta/<int:id>')
def ver_receta(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, c.nombre as categoria,
               CASE WHEN u.id = 1 THEN 'My Cooking' ELSE u.nombre_usuario END as autor,
               u.id as autor_id,
               COUNT(l.usuario_id) as likes_count
        FROM recetas r
        LEFT JOIN categorias c ON r.id_categoria = c.id
        LEFT JOIN usuarios u ON r.id_usuario = u.id
        LEFT JOIN likes l ON r.id = l.receta_id
        WHERE r.id = ?
        GROUP BY r.id
    """, (id,))
    receta = cursor.fetchone()

    if not receta:
        flash('Receta no encontrada.', 'error')
        return redirect(url_for('index'))

    # Verificar si el usuario actual ya dio like y si es favorito
    tiene_like = False
    es_favorito = False
    if 'user_id' in session:
        cursor.execute("SELECT * FROM likes WHERE usuario_id = ? AND receta_id = ?",
                      (session['user_id'], id))
        tiene_like = cursor.fetchone() is not None

        cursor.execute("SELECT * FROM favoritos WHERE usuario_id = ? AND receta_id = ?",
                      (session['user_id'], id))
        es_favorito = cursor.fetchone() is not None

    conn.close()
    return render_template('receta_detalle.html', receta=receta, tiene_like=tiene_like, es_favorito=es_favorito)

# Dar like a una receta y agregar a favoritos
@app.route('/receta/<int:id>/like', methods=['POST'])
@login_required
def dar_like(id):
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO likes (usuario_id, receta_id) VALUES (?, ?)",
            (session['user_id'], id)
        )
        conn.commit()
        flash('¡Te gusta esta receta!', 'success')
    except sqlite3.IntegrityError:
        flash('Ya diste like a esta receta.', 'info')

    # Agregar a favoritos
    try:
        cursor.execute(
            "INSERT INTO favoritos (usuario_id, receta_id) VALUES (?, ?)",
            (session['user_id'], id)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

    return redirect(url_for('ver_receta', id=id))

# Quitar like a una receta
@app.route('/receta/<int:id>/unlike', methods=['POST'])
@login_required
def quitar_like(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM likes WHERE usuario_id = ? AND receta_id = ?",
        (session['user_id'], id)
    )
    cursor.execute(
        "DELETE FROM favoritos WHERE usuario_id = ? AND receta_id = ?",
        (session['user_id'], id)
    )
    conn.commit()
    conn.close()

    flash('Like eliminado y receta quitada de favoritos.', 'info')
    return redirect(url_for('ver_receta', id=id))

# Mis favoritos
@app.route('/mis-favoritos')
@login_required
def mis_favoritos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, c.nombre as categoria,
               CASE WHEN u.id = 1 THEN 'My Cooking' ELSE u.nombre_usuario END as autor,
               u.id as autor_id,
               COUNT(l.usuario_id) as likes_count
        FROM recetas r
        LEFT JOIN categorias c ON r.id_categoria = c.id
        LEFT JOIN usuarios u ON r.id_usuario = u.id
        LEFT JOIN likes l ON r.id = l.receta_id
        WHERE r.id IN (
            SELECT receta_id FROM favoritos WHERE usuario_id = ?
        )
        GROUP BY r.id
        ORDER BY r.id DESC
    """, (session['user_id'],))
    favoritos = cursor.fetchall()
    conn.close()
    return render_template('favoritos.html', favoritos=favoritos)

# Agregar a favoritos
@app.route('/receta/<int:id>/favorito', methods=['POST'])
@login_required
def agregar_favorito(id):
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO favoritos (usuario_id, receta_id) VALUES (?, ?)",
            (session['user_id'], id)
        )
        conn.commit()
        flash('Receta agregada a favoritos.', 'success')
    except sqlite3.IntegrityError:
        flash('Esta receta ya está en tus favoritos.', 'info')
    finally:
        conn.close()

    return redirect(url_for('ver_receta', id=id))

# Quitar de favoritos
@app.route('/receta/<int:id>/no-favorito', methods=['POST'])
@login_required
def quitar_favorito(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM favoritos WHERE usuario_id = ? AND receta_id = ?",
        (session['user_id'], id)
    )
    conn.commit()
    conn.close()

    flash('Receta eliminada de favoritos.', 'info')
    return redirect(url_for('mis_favoritos'))

# Perfil de usuario
@app.route('/perfil/<int:id>')
def perfil_usuario(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre_usuario, email FROM usuarios WHERE id = ?", (id,))
    usuario = cursor.fetchone()

    if not usuario:
        flash('Usuario no encontrado.', 'error')
        return redirect(url_for('index'))

    cursor.execute("""
        SELECT r.*, c.nombre as categoria,
               COUNT(l.usuario_id) as likes_count
        FROM recetas r
        LEFT JOIN categorias c ON r.id_categoria = c.id
        LEFT JOIN likes l ON r.id = l.receta_id
        WHERE r.id_usuario = ?
        GROUP BY r.id
        ORDER BY r.id DESC
    """, (id,))
    recetas = cursor.fetchall()
    conn.close()

    return render_template('perfil.html', usuario=usuario, recetas=recetas)

# Buscar recetas
@app.route('/buscar')
def buscar_recetas():
    query = request.args.get('q', '')

    conn = get_db()
    cursor = conn.cursor()

    if query:
        cursor.execute("""
            SELECT r.*, c.nombre as categoria,
                   CASE WHEN u.id = 1 THEN 'My Cooking' ELSE u.nombre_usuario END as autor,
                   u.id as autor_id,
                   COUNT(l.usuario_id) as likes_count
            FROM recetas r
            LEFT JOIN categorias c ON r.id_categoria = c.id
            LEFT JOIN usuarios u ON r.id_usuario = u.id
            LEFT JOIN likes l ON r.id = l.receta_id
            WHERE r.titulo LIKE ? OR r.descripcion LIKE ? OR r.ingredientes LIKE ?
            GROUP BY r.id
            ORDER BY r.id DESC
        """, (f'%{query}%', f'%{query}%', f'%{query}%'))
    else:
        cursor.execute("""
            SELECT r.*, c.nombre as categoria,
                   CASE WHEN u.id = 1 THEN 'My Cooking' ELSE u.nombre_usuario END as autor,
                   u.id as autor_id,
                   COUNT(l.usuario_id) as likes_count
            FROM recetas r
            LEFT JOIN categorias c ON r.id_categoria = c.id
            LEFT JOIN usuarios u ON r.id_usuario = u.id
            LEFT JOIN likes l ON r.id = l.receta_id
            GROUP BY r.id
            ORDER BY r.id DESC
        """)

    recetas = cursor.fetchall()
    conn.close()

    return render_template('buscar.html', recetas=recetas, query=query)

if __name__ == '__main__':
    app.run(debug=True)
