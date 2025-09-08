from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'pemex-sistema-secreto-2025')

# Configuración de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 
    'mysql+mysqlconnector://root:root@localhost:3306/sistema_pemex')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Importar db y modelos
from models import (db, Usuario, ReporteAccionPreventiva, TipoReporte, 
                   OficinaRegional, EntidadFederativa, Municipio, ActorInterno, 
                   TipoAtencion, AccionPreventiva, SeguimientoAccion)

# Inicializar extensiones
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'

# Primero definir los modelos
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        usuario = Usuario.query.filter_by(username=username).first()
        
        if usuario and check_password_hash(usuario.password_hash, password):
            login_user(usuario)
            # Guardar información en sesión para el dashboard
            session['rol'] = usuario.rol
            session['nombre_completo'] = f"{usuario.nombre} {usuario.apellido_paterno} {usuario.apellido_materno}".strip()
            session['username'] = usuario.username
            
            next_page = request.args.get('next')
            if usuario.rol == 'administrador':
                return redirect(next_page) if next_page else redirect(url_for('admin_dashboard'))
            else:
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            error = 'Usuario o contraseña incorrectos'
    
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Obtener estadísticas para el dashboard
    stats = {
        'total_reportes': ReporteAccionPreventiva.query.count(),
        'en_proceso': ReporteAccionPreventiva.query.join(ReporteAccionPreventiva.estatus_actual).filter_by(nombre='En proceso').count() if ReporteAccionPreventiva.query.first() else 0,
        'atendidos': ReporteAccionPreventiva.query.join(ReporteAccionPreventiva.estatus_actual).filter_by(nombre='Atendido').count() if ReporteAccionPreventiva.query.first() else 0,
        'este_mes': ReporteAccionPreventiva.query.filter(
            ReporteAccionPreventiva.fecha_reporte >= date.today().replace(day=1)
        ).count() if ReporteAccionPreventiva.query.first() else 0
    }
    
    # Obtener estadísticas de acciones preventivas
    stats_acciones = {
        'total_acciones': AccionPreventiva.query.count(),
        'acciones_completadas': AccionPreventiva.query.filter_by(estado_accion='Completado').count(),
        'acciones_proceso': AccionPreventiva.query.filter_by(estado_accion='En Proceso').count(),
        'acciones_registradas': AccionPreventiva.query.filter_by(estado_accion='Registrado').count(),
        'acciones_mes': AccionPreventiva.query.filter(
            AccionPreventiva.fecha_registro >= date.today().replace(day=1)
        ).count()
    }
    
    # Obtener reportes recientes
    reportes_recientes = ReporteAccionPreventiva.query.order_by(
        ReporteAccionPreventiva.fecha_creacion.desc()
    ).limit(5).all()
    
    # Obtener acciones recientes
    acciones_recientes = AccionPreventiva.query.order_by(
        AccionPreventiva.fecha_creacion.desc()
    ).limit(5).all()
    
    return render_template('dashboard.html', stats=stats, stats_acciones=stats_acciones, 
                         reportes_recientes=reportes_recientes, acciones_recientes=acciones_recientes)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Verificar que el usuario sea administrador
    if current_user.rol != 'administrador':
        flash('No tienes permisos para acceder a esta área', 'error')
        return redirect(url_for('dashboard'))
    
    # Estadísticas para el dashboard administrativo
    total_acciones = AccionPreventiva.query.count()
    acciones_completadas = AccionPreventiva.query.filter_by(estado_accion='Completado').count()
    acciones_en_proceso = AccionPreventiva.query.filter_by(estado_accion='En Proceso').count()
    acciones_pendientes = AccionPreventiva.query.filter_by(estado_accion='Registrado').count()
    acciones_vencidas = AccionPreventiva.query.filter(
        AccionPreventiva.fecha_limite < date.today(),
        AccionPreventiva.estado_accion != 'Completado'
    ).count()
    
    # Acciones recientes para la tabla
    acciones_recientes = AccionPreventiva.query.order_by(
        AccionPreventiva.fecha_creacion.desc()
    ).limit(10).all()
    
    # Datos para gráficos - acciones por mes (últimos 6 meses)
    from collections import defaultdict
    from dateutil.relativedelta import relativedelta
    
    acciones_por_mes = defaultdict(int)
    for i in range(6):
        fecha = date.today() - relativedelta(months=i)
        mes_nombre = fecha.strftime('%b %Y')
        cantidad = AccionPreventiva.query.filter(
            AccionPreventiva.fecha_registro >= fecha.replace(day=1),
            AccionPreventiva.fecha_registro < (fecha.replace(day=1) + relativedelta(months=1))
        ).count()
        acciones_por_mes[mes_nombre] = cantidad
    
    return render_template('admin_dashboard.html',
                         total_acciones=total_acciones,
                         acciones_completadas=acciones_completadas,
                         acciones_en_proceso=acciones_en_proceso,
                         acciones_pendientes=acciones_pendientes,
                         acciones_vencidas=acciones_vencidas,
                         acciones_recientes=acciones_recientes,
                         acciones_por_mes=dict(acciones_por_mes))

@app.route('/registro-reporte')
@login_required
def registro_reporte():
    return render_template('registro_reporte.html')

@app.route('/seguimiento-acuerdos')
@login_required
def seguimiento_acuerdos():
    return render_template('seguimiento_acuerdos.html')

@app.route('/reportes')
@login_required
def reportes():
    return render_template('reportes.html')

@app.route('/admin')
@login_required
def admin():
    if current_user.rol != 'Administrador':
        flash('No tienes permisos para acceder a esta página', 'error')
        return redirect(url_for('dashboard'))
    return render_template('admin.html')

# API endpoints para formularios
@app.route('/api/registro_reporte', methods=['POST'])
@login_required
def api_registro_reporte():
    try:
        data = request.json
        
        # Validar datos requeridos
        campos_requeridos = ['tipo_reporte', 'oficina_regional', 'entidad_federativa', 
                           'municipio', 'fecha_solicitud', 'actor_interno', 'tipo_atencion']
        
        for campo in campos_requeridos:
            if not data.get(campo):
                return jsonify({'success': False, 'error': f'El campo {campo} es requerido'})
        
        # Generar folio automático
        tipo_abrev = {
            'Acción Preventiva': 'AP',
            'Problemática Social': 'PS',
            'Contingencia': 'CON'
        }
        
        oficina_abrev = db.session.query(OficinaRegional).filter_by(
            nombre=data['oficina_regional']
        ).first().abreviacion
        
        ultimo_reporte = db.session.query(ReporteAccionPreventiva).filter(
            ReporteAccionPreventiva.folio.like(f"{oficina_abrev}-{tipo_abrev[data['tipo_reporte']]}-%")
        ).order_by(ReporteAccionPreventiva.id.desc()).first()
        
        if ultimo_reporte:
            ultimo_numero = int(ultimo_reporte.folio.split('-')[-1])
            nuevo_numero = ultimo_numero + 1
        else:
            nuevo_numero = 1
            
        folio = f"{oficina_abrev}-{tipo_abrev[data['tipo_reporte']]}-{nuevo_numero:03d}"
        
        # Crear nuevo reporte
        nuevo_reporte = ReporteAccionPreventiva(
            folio=folio,
            tipo_reporte_id=db.session.query(TipoReporte).filter_by(nombre=data['tipo_reporte']).first().id,
            oficina_regional_id=db.session.query(OficinaRegional).filter_by(nombre=data['oficina_regional']).first().id,
            entidad_federativa_id=db.session.query(EntidadFederativa).filter_by(nombre=data['entidad_federativa']).first().id,
            municipio_id=db.session.query(Municipio).filter_by(nombre=data['municipio']).first().id,
            fecha_solicitud=datetime.strptime(data['fecha_solicitud'], '%Y-%m-%d').date(),
            actor_interno_id=db.session.query(ActorInterno).filter_by(nombre=data['actor_interno']).first().id,
            tipo_atencion_id=db.session.query(TipoAtencion).filter_by(nombre=data['tipo_atencion']).first().id,
            solicitante=data.get('solicitante', ''),
            causa_motivo=data.get('causa_motivo', ''),
            descripcion_hechos=data.get('descripcion_hechos', ''),
            fecha_compromiso=datetime.strptime(data['fecha_compromiso'], '%Y-%m-%d').date() if data.get('fecha_compromiso') else None,
            observaciones=data.get('observaciones', ''),
            usuario_id=current_user.id,
            estado='Borrador' if data.get('guardar_borrador') else 'Registrado'
        )
        
        db.session.add(nuevo_reporte)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Reporte guardado exitosamente',
            'folio': folio,
            'id': nuevo_reporte.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# ==========================================
# RUTAS PARA FORMULARIO DE ACCIONES PREVENTIVAS
# ==========================================

@app.route('/formulario_accion')
@login_required
def formulario_accion():
    """Formulario para registrar nueva acción preventiva"""
    return render_template('formulario_accion.html')

@app.route('/acciones')
@login_required
def acciones():
    """Listado de acciones preventivas"""
    acciones = AccionPreventiva.query.order_by(AccionPreventiva.fecha_creacion.desc()).all()
    return render_template('acciones.html', acciones=acciones)

@app.route('/acciones/<int:id>')
@login_required
def ver_accion(id):
    """Ver detalle de una acción preventiva"""
    accion = AccionPreventiva.query.get_or_404(id)
    return render_template('ver_accion.html', accion=accion)

@app.route('/api/acciones', methods=['POST'])
@login_required
def crear_accion():
    """API para crear nueva acción preventiva"""
    try:
        data = request.form.to_dict()
        
        # Generar folio único si no se proporciona
        folio = data.get('folio')
        if not folio:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            folio = f"AP-{timestamp}"
        
        # Validar que el folio no exista
        if db.session.query(AccionPreventiva).filter_by(folio=folio).first():
            return jsonify({'success': False, 'message': 'El folio ya existe'})
        
        # Crear nueva acción preventiva
        nueva_accion = AccionPreventiva(
            folio=folio,
            fecha_registro=datetime.strptime(data['fecha_registro'], '%Y-%m-%d').date(),
            region=data['region'],
            activo=data['activo'],
            instalacion=data['instalacion'],
            estado=data['estado'],
            municipio=data['municipio'],
            localidad=data['localidad'],
            coordenadas_x=float(data['coordenadas_x']) if data.get('coordenadas_x') else None,
            coordenadas_y=float(data['coordenadas_y']) if data.get('coordenadas_y') else None,
            tipo_problematica=data['tipo_problematica'],
            descripcion_problematica=data['descripcion_problematica'],
            actor_social=data['actor_social'],
            nivel_impacto=data['nivel_impacto'],
            accion_preventiva=data['accion_preventiva'],
            fecha_inicio=datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date(),
            fecha_fin=datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date(),
            presupuesto=float(data['presupuesto']) if data.get('presupuesto') else None,
            responsable=data['responsable'],
            area_responsable=data['area_responsable'],
            observaciones=data.get('observaciones', ''),
            usuario_id=current_user.id,
            estado_accion='Registrado'
        )
        
        db.session.add(nueva_accion)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Acción preventiva registrada exitosamente',
            'folio': folio,
            'id': nueva_accion.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/acciones/borrador', methods=['POST'])
@login_required
def guardar_borrador_accion():
    """API para guardar borrador de acción preventiva"""
    try:
        data = request.form.to_dict()
        
        # Generar folio único si no se proporciona
        folio = data.get('folio')
        if not folio:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            folio = f"AP-DRAFT-{timestamp}"
        
        # Crear borrador
        borrador_accion = AccionPreventiva(
            folio=folio,
            fecha_registro=datetime.strptime(data['fecha_registro'], '%Y-%m-%d').date() if data.get('fecha_registro') else datetime.now().date(),
            region=data.get('region', ''),
            activo=data.get('activo', ''),
            instalacion=data.get('instalacion', ''),
            estado=data.get('estado', ''),
            municipio=data.get('municipio', ''),
            localidad=data.get('localidad', ''),
            coordenadas_x=float(data['coordenadas_x']) if data.get('coordenadas_x') else None,
            coordenadas_y=float(data['coordenadas_y']) if data.get('coordenadas_y') else None,
            tipo_problematica=data.get('tipo_problematica', ''),
            descripcion_problematica=data.get('descripcion_problematica', ''),
            actor_social=data.get('actor_social', ''),
            nivel_impacto=data.get('nivel_impacto', ''),
            accion_preventiva=data.get('accion_preventiva', ''),
            fecha_inicio=datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date() if data.get('fecha_inicio') else None,
            fecha_fin=datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date() if data.get('fecha_fin') else None,
            presupuesto=float(data['presupuesto']) if data.get('presupuesto') else None,
            responsable=data.get('responsable', ''),
            area_responsable=data.get('area_responsable', ''),
            observaciones=data.get('observaciones', ''),
            usuario_id=current_user.id,
            estado_accion='Borrador'
        )
        
        db.session.add(borrador_accion)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Borrador guardado exitosamente',
            'folio': folio,
            'id': borrador_accion.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/seguimiento_accion', methods=['POST'])
@login_required
def api_seguimiento_accion():
    """API para registrar seguimiento de acción preventiva"""
    try:
        data = request.form.to_dict()
        
        # Validar datos requeridos
        if not data.get('accion_id'):
            return jsonify({'success': False, 'message': 'ID de acción es requerido'})
        
        # Buscar la acción
        accion = AccionPreventiva.query.get(data['accion_id'])
        if not accion:
            return jsonify({'success': False, 'message': 'Acción no encontrada'})
        
        # Crear seguimiento
        seguimiento = SeguimientoAccion(
            accion_id=accion.id,
            fecha_seguimiento=datetime.strptime(data['fecha_seguimiento'], '%Y-%m-%d').date(),
            estado_anterior=data.get('estado_anterior', accion.estado_accion),
            estado_nuevo=data['estado_nuevo'],
            porcentaje_avance=int(data['porcentaje_avance']),
            observaciones=data.get('observaciones', ''),
            responsable=data['responsable'],
            usuario_id=current_user.id
        )
        
        # Actualizar la acción
        accion.estado_accion = data['estado_nuevo']
        accion.porcentaje_avance = int(data['porcentaje_avance'])
        accion.fecha_ultima_actualizacion = datetime.now().date()
        
        db.session.add(seguimiento)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Seguimiento registrado exitosamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/seguimiento_compromiso', methods=['POST'])
@login_required  
def api_seguimiento_compromiso():
    try:
        data = request.json
        
        # Validar datos requeridos
        if not data.get('reporte_id'):
            return jsonify({'success': False, 'error': 'ID de reporte es requerido'})
            
        # Buscar el reporte
        reporte = ReporteAccionPreventiva.query.get(data['reporte_id'])
        if not reporte:
            return jsonify({'success': False, 'error': 'Reporte no encontrado'})
        
        # Crear seguimiento de compromiso
        seguimiento = SeguimientoAccion(
            reporte_id=reporte.id,
            fecha_seguimiento=datetime.now().date(),
            avance_porcentaje=data.get('avance_porcentaje', 0),
            observaciones=data.get('observaciones', ''),
            evidencias=data.get('evidencias', ''),
            usuario_id=current_user.id
        )
        
        # Actualizar estado del reporte basado en el avance
        if data.get('avance_porcentaje') == 100:
            reporte.estado = 'Completado'
        elif data.get('avance_porcentaje') > 0:
            reporte.estado = 'En Progreso'
        
        db.session.add(seguimiento)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Seguimiento guardado exitosamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/buscar_reporte/<folio>')
@login_required
def api_buscar_reporte(folio):
    try:
        reporte = ReporteAccionPreventiva.query.filter_by(folio=folio).first()
        if not reporte:
            return jsonify({'success': False, 'error': 'Reporte no encontrado'})
        
        # Obtener seguimientos
        seguimientos = SeguimientoAccion.query.filter_by(accion_id=reporte.id).all()
        
        return jsonify({
            'success': True,
            'reporte': {
                'id': reporte.id,
                'folio': reporte.folio,
                'tipo_reporte': reporte.tipo_reporte.nombre,
                'solicitante': reporte.solicitante,
                'causa_motivo': reporte.causa_motivo,
                'descripcion_hechos': reporte.descripcion_hechos,
                'fecha_compromiso': reporte.fecha_compromiso.strftime('%Y-%m-%d') if reporte.fecha_compromiso else '',
                'estado': reporte.estado,
                'seguimientos': [{
                    'fecha': s.fecha_seguimiento.strftime('%Y-%m-%d'),
                    'avance': s.avance_porcentaje,
                    'observaciones': s.observaciones
                } for s in seguimientos]
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API endpoints para catálogos
@app.route('/api/catalogos/oficinas_regionales')
@login_required
def api_oficinas_regionales():
    oficinas = OficinaRegional.query.all()
    return jsonify([{'id': o.id, 'nombre': o.nombre, 'abreviacion': o.abreviacion} for o in oficinas])

@app.route('/api/catalogos/tipos_reporte')
@login_required
def api_tipos_reporte():
    tipos = TipoReporte.query.all()
    return jsonify([{'id': t.id, 'nombre': t.nombre} for t in tipos])

@app.route('/api/catalogos/entidades_federativas')
@login_required
def api_entidades_federativas():
    entidades = EntidadFederativa.query.all()
    return jsonify([{'id': e.id, 'nombre': e.nombre} for e in entidades])

@app.route('/api/catalogos/municipios/<int:entidad_id>')
@login_required
def api_municipios(entidad_id):
    municipios = Municipio.query.filter_by(entidad_federativa_id=entidad_id).all()
    return jsonify([{'id': m.id, 'nombre': m.nombre} for m in municipios])

@app.route('/api/catalogos/actores_internos')
@login_required
def api_actores_internos():
    actores = ActorInterno.query.all()
    return jsonify([{'id': a.id, 'nombre': a.nombre} for a in actores])

@app.route('/api/catalogos/tipos_atencion')
@login_required
def api_tipos_atencion():
    tipos = TipoAtencion.query.all()
    return jsonify([{'id': t.id, 'nombre': t.nombre} for t in tipos])

# ========== GESTIÓN DE USUARIOS ==========

@app.route('/admin/usuarios')
@login_required
def admin_usuarios():
    """Vista principal de gestión de usuarios"""
    if current_user.rol != 'Administrador':
        flash('No tienes permisos para acceder a esta sección', 'error')
        return redirect(url_for('dashboard'))
    
    usuarios = Usuario.query.filter_by(activo=True).order_by(Usuario.fecha_creacion.desc()).all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@app.route('/api/usuarios', methods=['GET'])
@login_required
def api_usuarios_listar():
    """API para listar usuarios"""
    if current_user.rol != 'Administrador':
        return jsonify({'success': False, 'error': 'No autorizado'})
    
    usuarios = Usuario.query.filter_by(activo=True).all()
    return jsonify({
        'success': True,
        'usuarios': [usuario.to_dict() for usuario in usuarios]
    })

@app.route('/api/usuarios', methods=['POST'])
@login_required
def api_usuarios_crear():
    """API para crear nuevo usuario"""
    if current_user.rol != 'Administrador':
        return jsonify({'success': False, 'error': 'No autorizado'})
    
    try:
        data = request.json
        
        # Validaciones básicas
        if not data.get('username') or not data.get('password'):
            return jsonify({'success': False, 'error': 'Username y password son requeridos'})
        
        if not data.get('email') or not data.get('nombre') or not data.get('apellido_paterno'):
            return jsonify({'success': False, 'error': 'Email, nombre y apellido paterno son requeridos'})
        
        # Verificar que el username no exista
        usuario_existente = Usuario.query.filter_by(username=data['username']).first()
        if usuario_existente:
            return jsonify({'success': False, 'error': 'El nombre de usuario ya existe'})
        
        # Verificar que el email no exista
        email_existente = Usuario.query.filter_by(email=data['email']).first()
        if email_existente:
            return jsonify({'success': False, 'error': 'El correo electrónico ya está registrado'})
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            username=data['username'],
            email=data['email'],
            nombre=data['nombre'],
            apellido_paterno=data['apellido_paterno'],
            apellido_materno=data.get('apellido_materno', ''),
            telefono=data.get('telefono', ''),
            puesto=data.get('puesto', ''),
            rol=data.get('rol', 'Capturista')
        )
        
        nuevo_usuario.set_password(data['password'])
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuario creado exitosamente',
            'usuario': nuevo_usuario.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/usuarios/<int:usuario_id>', methods=['GET'])
@login_required
def api_obtener_usuario(usuario_id):
    """API para obtener datos de un usuario específico"""
    if current_user.rol != 'Administrador':
        return jsonify({'success': False, 'error': 'No autorizado'})
    
    try:
        usuario = Usuario.query.get_or_404(usuario_id)
        return jsonify({
            'success': True,
            'usuario': usuario.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/usuarios/<int:usuario_id>', methods=['PUT'])
@login_required
def api_usuarios_actualizar(usuario_id):
    """API para actualizar usuario"""
    if current_user.rol != 'Administrador':
        return jsonify({'success': False, 'error': 'No autorizado'})
    
    try:
        usuario = Usuario.query.get_or_404(usuario_id)
        data = request.json
        
        # Verificar cambios de username y email
        if data.get('username') and data['username'] != usuario.username:
            username_existente = Usuario.query.filter_by(username=data['username']).first()
            if username_existente:
                return jsonify({'success': False, 'error': 'El nombre de usuario ya existe'})
            usuario.username = data['username']
        
        if data.get('email') and data['email'] != usuario.email:
            email_existente = Usuario.query.filter_by(email=data['email']).first()
            if email_existente:
                return jsonify({'success': False, 'error': 'El correo electrónico ya está registrado'})
            usuario.email = data['email']
        
        # Actualizar otros campos
        if data.get('nombre'):
            usuario.nombre = data['nombre']
        if data.get('apellido_paterno'):
            usuario.apellido_paterno = data['apellido_paterno']
        if 'apellido_materno' in data:
            usuario.apellido_materno = data['apellido_materno']
        if 'telefono' in data:
            usuario.telefono = data['telefono']
        if 'puesto' in data:
            usuario.puesto = data['puesto']
        if data.get('rol'):
            usuario.rol = data['rol']
        
        # Cambiar contraseña si se proporciona
        if data.get('password'):
            usuario.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuario actualizado exitosamente',
            'usuario': usuario.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/usuarios/<int:usuario_id>', methods=['DELETE'])
@login_required
def api_usuarios_eliminar(usuario_id):
    """API para eliminar (desactivar) usuario"""
    if current_user.rol != 'Administrador':
        return jsonify({'success': False, 'error': 'No autorizado'})
    
    try:
        usuario = Usuario.query.get_or_404(usuario_id)
        
        # No permitir eliminar el propio usuario
        if usuario.id == current_user.id:
            return jsonify({'success': False, 'error': 'No puedes eliminar tu propio usuario'})
        
        # Desactivar usuario en lugar de eliminarlo
        usuario.activo = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuario desactivado exitosamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/usuarios/activos')
@login_required
def api_usuarios_activos():
    """API para obtener lista de usuarios activos para selección"""
    usuarios = Usuario.query.filter_by(activo=True).order_by(Usuario.nombre, Usuario.apellido_paterno).all()
    return jsonify([{
        'id': u.id,
        'nombre_completo': u.nombre_completo,
        'username': u.username,
        'puesto': u.puesto
    } for u in usuarios])

@app.route('/api/estadisticas-admin')
@login_required
def api_estadisticas_admin():
    """API para obtener estadísticas del sistema para administradores"""
    if current_user.rol != 'Administrador':
        return jsonify({'success': False, 'error': 'No autorizado'})
    
    try:
        # Contar usuarios activos
        total_usuarios = Usuario.query.filter_by(activo=True).count()
        
        # Reportes de este mes
        primer_dia_mes = date.today().replace(day=1)
        reportes_mes = ReporteAccionPreventiva.query.filter(
            ReporteAccionPreventiva.fecha_reporte >= primer_dia_mes
        ).count()
        
        # Acuerdos pendientes (ejemplo - ajustar según modelo real)
        acuerdos_pendientes = 0  # Implementar cuando esté el modelo de seguimiento
        
        # Último acceso (simplificado)
        ultimo_acceso = "Hoy"
        
        return jsonify({
            'success': True,
            'estadisticas': {
                'usuarios': total_usuarios,
                'reportes_mes': reportes_mes,
                'acuerdos_pendientes': acuerdos_pendientes,
                'ultimo_acceso': ultimo_acceso
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ========== FUNCIONES DE UTILIDAD ==========

@app.context_processor
def utility_processor():
    """Funciones disponibles en todas las plantillas"""
    return dict(
        current_year=datetime.now().year,
        current_date=date.today()
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
