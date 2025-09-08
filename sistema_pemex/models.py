from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Numeric

# Esta instancia se importará en app.py
db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Información personal completa según requerimientos
    nombre = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    puesto = db.Column(db.String(150), nullable=True)
    
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False, default='Capturista')  # Administrador o Capturista
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_ultimo_acceso = db.Column(db.DateTime)
    
    # Relaciones
    reportes = db.relationship('ReporteAccionPreventiva', backref='responsable_captura', lazy=True)
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del usuario"""
        nombres = [self.nombre, self.apellido_paterno]
        if self.apellido_materno:
            nombres.append(self.apellido_materno)
        return ' '.join(nombres)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convierte el usuario a diccionario para JSON"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'nombre': self.nombre,
            'apellido_paterno': self.apellido_paterno,
            'apellido_materno': self.apellido_materno,
            'telefono': self.telefono,
            'puesto': self.puesto,
            'rol': self.rol,
            'activo': self.activo,
            'nombre_completo': self.nombre_completo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
    
    def __repr__(self):
        return f'<Usuario {self.username}>'

# Catálogos
class OficinaRegional(db.Model):
    __tablename__ = 'cat_oficina_regional'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    abreviatura = db.Column(db.String(10), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    entidades = db.relationship('EntidadFederativa', backref='oficina_regional', lazy=True)
    reportes = db.relationship('ReporteAccionPreventiva', backref='oficina_regional', lazy=True)

class TipoReporte(db.Model):
    __tablename__ = 'cat_tipo_reporte'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    abreviatura = db.Column(db.String(10), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    reportes = db.relationship('ReporteAccionPreventiva', backref='tipo_reporte', lazy=True)

class EntidadFederativa(db.Model):
    __tablename__ = 'cat_entidad_federativa'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    abreviatura = db.Column(db.String(10), nullable=False)
    oficina_regional_id = db.Column(db.Integer, db.ForeignKey('cat_oficina_regional.id'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    municipios = db.relationship('Municipio', backref='entidad_federativa', lazy=True)
    reportes = db.relationship('ReporteAccionPreventiva', backref='entidad_federativa', lazy=True)

class Municipio(db.Model):
    __tablename__ = 'cat_municipio'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    entidad_federativa_id = db.Column(db.Integer, db.ForeignKey('cat_entidad_federativa.id'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    reportes = db.relationship('ReporteAccionPreventiva', backref='municipio', lazy=True)

class TipoAtencion(db.Model):
    __tablename__ = 'cat_tipo_atencion'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    activo = db.Column(db.Boolean, default=True)

class ActorInterno(db.Model):
    __tablename__ = 'cat_actor_interno'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    reportes = db.relationship('ReporteAccionPreventiva', backref='actor_interno', lazy=True)

class TipoProblematica(db.Model):
    __tablename__ = 'cat_tipo_problematica'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    reportes = db.relationship('ReporteAccionPreventiva', backref='tipo_problematica', lazy=True)

class GradoClasificacion(db.Model):
    __tablename__ = 'cat_grado_clasificacion'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    reportes = db.relationship('ReporteAccionPreventiva', backref='grado_clasificacion', lazy=True)

class EstatusGeneral(db.Model):
    __tablename__ = 'cat_estatus_general'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'reporte', 'cumplimiento', 'probabilidad'
    activo = db.Column(db.Boolean, default=True)

# Tabla principal de reportes
class ReporteAccionPreventiva(db.Model):
    __tablename__ = 'reportes_accion_preventiva'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_registro = db.Column(db.Integer, unique=True, nullable=False)
    
    # Campos básicos
    responsable_captura_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    oficina_regional_id = db.Column(db.Integer, db.ForeignKey('cat_oficina_regional.id'), nullable=False)
    año_reporte = db.Column(db.Integer, nullable=False, default=lambda: datetime.now().year)
    folio = db.Column(db.String(50), unique=True, nullable=False)
    tipo_reporte_id = db.Column(db.Integer, db.ForeignKey('cat_tipo_reporte.id'), nullable=False)
    fecha_reporte = db.Column(db.Date, nullable=False, default=date.today)
    
    # Ubicación
    entidad_federativa_id = db.Column(db.Integer, db.ForeignKey('cat_entidad_federativa.id'), nullable=False)
    municipio_id = db.Column(db.Integer, db.ForeignKey('cat_municipio.id'), nullable=False)
    
    # Fechas específicas
    fecha_inicio_problematica = db.Column(db.Date)  # Solo para PROBLEMÁTICA SOCIAL o CONFLICTO
    fecha_obtencion_lso = db.Column(db.Date)  # Solo para CONFLICTO
    dias_duracion_cierre = db.Column(db.Integer)  # Calculado
    
    # Descripción del evento
    descripcion_evento = db.Column(db.Text, nullable=False)
    exigencia_reclamacion = db.Column(db.Text, nullable=False)
    impacto_no_atender = db.Column(db.Text, nullable=False)
    acciones_realizar = db.Column(db.Text, nullable=False)
    
    # Tipos de atención (múltiple)
    tipos_atencion = db.Column(db.Text)  # JSON con los IDs seleccionados
    otro_tipo_atencion = db.Column(db.Text)
    
    # Compromisos y acuerdos
    compromisos_acuerdos = db.Column(db.Text)
    
    # Actores
    grupo_interes_localidad = db.Column(db.Text, nullable=False)
    representantes_lideres = db.Column(db.Text)
    actor_interno_id = db.Column(db.Integer, db.ForeignKey('cat_actor_interno.id'), nullable=False)
    otro_actor_interno = db.Column(db.Text)
    actores_externos = db.Column(db.Text)
    
    # Instalaciones y proyectos
    instalacion_estrategica = db.Column(db.Text, default='N/A')
    proyectos_relacionados = db.Column(db.Text, default='N/A')
    
    # Solo para PROBLEMÁTICA SOCIAL o CONFLICTO
    tipo_problematica_id = db.Column(db.Integer, db.ForeignKey('cat_tipo_problematica.id'))
    otro_tipo_problematica = db.Column(db.Text)
    area_involucrada = db.Column(db.Text)
    grado_clasificacion_id = db.Column(db.Integer, db.ForeignKey('cat_grado_clasificacion.id'))
    
    # Estatus
    descripcion_estatus_cierre = db.Column(db.Text)
    fecha_estatus_cierre = db.Column(db.Date)
    estatus_actual_id = db.Column(db.Integer, db.ForeignKey('cat_estatus_general.id'))
    grado_probabilidad_id = db.Column(db.Integer, db.ForeignKey('cat_estatus_general.id'))
    
    # Campos de auditoría
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    seguimientos = db.relationship('SeguimientoCompromiso', backref='reporte', lazy=True)
    historial_ediciones = db.relationship('HistorialEdicion', backref='reporte', lazy=True)
    
    def __repr__(self):
        return f'<ReporteAccionPreventiva {self.folio}>'

# Tabla de seguimiento de compromisos
class SeguimientoCompromiso(db.Model):
    __tablename__ = 'seguimiento_compromisos'
    
    id = db.Column(db.Integer, primary_key=True)
    reporte_id = db.Column(db.Integer, db.ForeignKey('reportes_accion_preventiva.id'), nullable=False)
    
    # Campos específicos del seguimiento
    estatus_cumplimiento = db.Column(db.Text)
    numero_proas = db.Column(db.Integer)
    ficha_dyd_cedula_pacma = db.Column(db.String(100))
    
    # Avances mensuales (JSON)
    avances_mensuales = db.Column(db.Text)  # JSON con los porcentajes de cada mes
    
    # Estatus calculado
    estatus_cumplimiento_final_id = db.Column(db.Integer, db.ForeignKey('cat_estatus_general.id'))
    
    # Campos de uso exclusivo SPV
    campo_spv_1 = db.Column(db.Text)
    campo_spv_2 = db.Column(db.Text)
    campo_spv_3 = db.Column(db.Text)
    campo_spv_4 = db.Column(db.Text)
    
    # Auditoría
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    responsable_captura_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

# Tabla para el historial de ediciones
class HistorialEdicion(db.Model):
    __tablename__ = 'historial_ediciones'
    
    id = db.Column(db.Integer, primary_key=True)
    reporte_id = db.Column(db.Integer, db.ForeignKey('reportes_accion_preventiva.id'), nullable=False)
    campo_editado = db.Column(db.String(100), nullable=False)
    valor_anterior = db.Column(db.Text)
    valor_nuevo = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_edicion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con usuario
    usuario = db.relationship('Usuario', backref='ediciones_realizadas')

# Tabla para tipos de atención seleccionados (relación muchos a muchos)
class ReporteTipoAtencion(db.Model):
    __tablename__ = 'reporte_tipo_atencion'
    
    id = db.Column(db.Integer, primary_key=True)
    reporte_id = db.Column(db.Integer, db.ForeignKey('reportes_accion_preventiva.id'), nullable=False)
    tipo_atencion_id = db.Column(db.Integer, db.ForeignKey('cat_tipo_atencion.id'), nullable=False)
    
    # Relaciones
    reporte = db.relationship('ReporteAccionPreventiva', backref='reporte_tipos_atencion')
    tipo_atencion = db.relationship('TipoAtencion', backref='reportes_asociados')

# ==========================================
# MODELO PARA ACCIONES PREVENTIVAS
# ==========================================

class AccionPreventiva(db.Model):
    __tablename__ = 'acciones_preventivas'
    
    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(50), unique=True, nullable=False)
    
    # Información general
    fecha_registro = db.Column(db.Date, nullable=False)
    region = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.String(100), nullable=False)
    instalacion = db.Column(db.String(200), nullable=False)
    
    # Ubicación geográfica
    estado = db.Column(db.String(100), nullable=False)
    municipio = db.Column(db.String(150), nullable=False)
    localidad = db.Column(db.String(150), nullable=False)
    coordenadas_x = db.Column(db.Float, nullable=True)
    coordenadas_y = db.Column(db.Float, nullable=True)
    
    # Problemática social
    tipo_problematica = db.Column(db.String(200), nullable=False)
    descripcion_problematica = db.Column(db.Text, nullable=False)
    actor_social = db.Column(db.String(200), nullable=False)
    nivel_impacto = db.Column(db.String(50), nullable=False)
    
    # Acción preventiva
    accion_preventiva = db.Column(db.Text, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    presupuesto = db.Column(Numeric(15, 2), nullable=True)
    responsable = db.Column(db.String(200), nullable=False)
    area_responsable = db.Column(db.String(200), nullable=False)
    
    # Documentos y observaciones
    observaciones = db.Column(db.Text, nullable=True)
    documento_1 = db.Column(db.String(255), nullable=True)
    documento_2 = db.Column(db.String(255), nullable=True)
    
    # Control y seguimiento
    estado_accion = db.Column(db.String(50), nullable=False, default='Registrado')  # Registrado, En Proceso, Completado, Cancelado, Borrador
    fecha_ultima_actualizacion = db.Column(db.Date, nullable=True)
    porcentaje_avance = db.Column(db.Integer, default=0)
    
    # Auditoría
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Relación con usuario
    usuario = db.relationship('Usuario', backref='acciones_preventivas')
    
    def to_dict(self):
        """Convierte la acción a diccionario para JSON"""
        return {
            'id': self.id,
            'folio': self.folio,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'region': self.region,
            'activo': self.activo,
            'instalacion': self.instalacion,
            'estado': self.estado,
            'municipio': self.municipio,
            'localidad': self.localidad,
            'coordenadas_x': float(self.coordenadas_x) if self.coordenadas_x else None,
            'coordenadas_y': float(self.coordenadas_y) if self.coordenadas_y else None,
            'tipo_problematica': self.tipo_problematica,
            'descripcion_problematica': self.descripcion_problematica,
            'actor_social': self.actor_social,
            'nivel_impacto': self.nivel_impacto,
            'accion_preventiva': self.accion_preventiva,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'presupuesto': float(self.presupuesto) if self.presupuesto else None,
            'responsable': self.responsable,
            'area_responsable': self.area_responsable,
            'observaciones': self.observaciones,
            'estado_accion': self.estado_accion,
            'fecha_ultima_actualizacion': self.fecha_ultima_actualizacion.isoformat() if self.fecha_ultima_actualizacion else None,
            'porcentaje_avance': self.porcentaje_avance,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'usuario_captura': self.usuario.nombre_completo if self.usuario else None
        }
    
    def __repr__(self):
        return f'<AccionPreventiva {self.folio}: {self.tipo_problematica}>'

# Tabla para seguimiento de acciones preventivas
class SeguimientoAccion(db.Model):
    __tablename__ = 'seguimiento_acciones'
    
    id = db.Column(db.Integer, primary_key=True)
    accion_id = db.Column(db.Integer, db.ForeignKey('acciones_preventivas.id'), nullable=False)
    fecha_seguimiento = db.Column(db.Date, nullable=False)
    estado_anterior = db.Column(db.String(50), nullable=False)
    estado_nuevo = db.Column(db.String(50), nullable=False)
    porcentaje_avance = db.Column(db.Integer, nullable=False, default=0)
    observaciones = db.Column(db.Text, nullable=True)
    responsable = db.Column(db.String(200), nullable=False)
    evidencia_documento = db.Column(db.String(255), nullable=True)
    
    # Auditoría
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Relaciones
    accion = db.relationship('AccionPreventiva', backref='seguimientos')
    usuario = db.relationship('Usuario', backref='seguimientos_realizados')
    
    def to_dict(self):
        return {
            'id': self.id,
            'accion_id': self.accion_id,
            'fecha_seguimiento': self.fecha_seguimiento.isoformat() if self.fecha_seguimiento else None,
            'estado_anterior': self.estado_anterior,
            'estado_nuevo': self.estado_nuevo,
            'porcentaje_avance': self.porcentaje_avance,
            'observaciones': self.observaciones,
            'responsable': self.responsable,
            'evidencia_documento': self.evidencia_documento,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'usuario_seguimiento': self.usuario.nombre_completo if self.usuario else None
        }
