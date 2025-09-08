"""
Script para inicializar la base de datos con datos iniciales
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sistema_pemex'))

from sistema_pemex.models import *
from werkzeug.security import generate_password_hash

def create_app():
    from flask import Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'pemex-sistema-secreto-2025'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/sistema_pemex'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    return app

def init_database():
    """Inicializar la base de datos con datos básicos"""
    
    app = create_app()
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("✓ Tablas creadas exitosamente")
        
        # Verificar si ya existen datos
        if Usuario.query.first():
            print("La base de datos ya contiene datos. No se insertarán datos duplicados.")
            return
        
        # 1. Crear oficinas regionales
        oficinas = [
            {'nombre': 'Oficina Regional Norte', 'abreviatura': 'ORN'},
            {'nombre': 'Oficina Regional Centro', 'abreviatura': 'ORC'},
            {'nombre': 'Oficina Regional Sur', 'abreviatura': 'ORS'},
            {'nombre': 'Oficina Regional Sureste', 'abreviatura': 'ORSE'},
            {'nombre': 'Oficina Regional Marina Noreste', 'abreviatura': 'ORMNE'},
            {'nombre': 'Oficina Regional Marina Suroeste', 'abreviatura': 'ORMSO'}
        ]
        
        for oficina_data in oficinas:
            oficina = OficinaRegional(**oficina_data)
            db.session.add(oficina)
        
        db.session.commit()
        print("✓ Oficinas regionales creadas")
        
        # 2. Crear tipos de reporte
        tipos_reporte = [
            {'nombre': 'Acción Preventiva', 'abreviatura': 'AP'},
            {'nombre': 'Problemática Social', 'abreviatura': 'PS'},
            {'nombre': 'Conflicto', 'abreviatura': 'CON'}
        ]
        
        for tipo_data in tipos_reporte:
            tipo = TipoReporte(**tipo_data)
            db.session.add(tipo)
        
        db.session.commit()
        print("✓ Tipos de reporte creados")
        
        # 3. Crear entidades federativas (algunas principales)
        entidades = [
            {'nombre': 'Ciudad de México', 'abreviatura': 'CDMX', 'oficina_regional_id': 2},
            {'nombre': 'Estado de México', 'abreviatura': 'EDOMEX', 'oficina_regional_id': 2},
            {'nombre': 'Nuevo León', 'abreviatura': 'NL', 'oficina_regional_id': 1},
            {'nombre': 'Jalisco', 'abreviatura': 'JAL', 'oficina_regional_id': 2},
            {'nombre': 'Veracruz', 'abreviatura': 'VER', 'oficina_regional_id': 4},
            {'nombre': 'Tabasco', 'abreviatura': 'TAB', 'oficina_regional_id': 4},
            {'nombre': 'Campeche', 'abreviatura': 'CAM', 'oficina_regional_id': 4},
            {'nombre': 'Chiapas', 'abreviatura': 'CHIS', 'oficina_regional_id': 3},
            {'nombre': 'Tamaulipas', 'abreviatura': 'TAMS', 'oficina_regional_id': 1},
            {'nombre': 'Coahuila', 'abreviatura': 'COAH', 'oficina_regional_id': 1}
        ]
        
        for entidad_data in entidades:
            entidad = EntidadFederativa(**entidad_data)
            db.session.add(entidad)
        
        db.session.commit()
        print("✓ Entidades federativas creadas")
        
        # 4. Crear algunos municipios de ejemplo
        municipios = [
            {'nombre': 'Benito Juárez', 'entidad_federativa_id': 1},
            {'nombre': 'Miguel Hidalgo', 'entidad_federativa_id': 1},
            {'nombre': 'Cuauhtémoc', 'entidad_federativa_id': 1},
            {'nombre': 'Naucalpan', 'entidad_federativa_id': 2},
            {'nombre': 'Tlalnepantla', 'entidad_federativa_id': 2},
            {'nombre': 'Monterrey', 'entidad_federativa_id': 3},
            {'nombre': 'San Nicolás', 'entidad_federativa_id': 3},
            {'nombre': 'Guadalajara', 'entidad_federativa_id': 4},
            {'nombre': 'Zapopan', 'entidad_federativa_id': 4},
            {'nombre': 'Veracruz', 'entidad_federativa_id': 5}
        ]
        
        for municipio_data in municipios:
            municipio = Municipio(**municipio_data)
            db.session.add(municipio)
        
        db.session.commit()
        print("✓ Municipios creados")
        
        # 5. Crear tipos de atención
        tipos_atencion = [
            {'nombre': 'Mesa de diálogo'},
            {'nombre': 'Reunión de trabajo'},
            {'nombre': 'Visita de campo'},
            {'nombre': 'Gestión ante autoridades'},
            {'nombre': 'Capacitación'},
            {'nombre': 'Entrega de apoyos'},
            {'nombre': 'Firma de convenio'},
            {'nombre': 'Otro'}
        ]
        
        for tipo_data in tipos_atencion:
            tipo = TipoAtencion(**tipo_data)
            db.session.add(tipo)
        
        db.session.commit()
        print("✓ Tipos de atención creados")
        
        # 6. Crear actores internos
        actores_internos = [
            {'nombre': 'Dirección General'},
            {'nombre': 'Subdirección de Desarrollo Social'},
            {'nombre': 'Subdirección de Producción'},
            {'nombre': 'Subdirección de Exploración'},
            {'nombre': 'Subdirección de Perforación'},
            {'nombre': 'Coordinación de Relaciones Institucionales'},
            {'nombre': 'Gerencia Regional'},
            {'nombre': 'Coordinación de Seguridad Física'},
            {'nombre': 'Otro'}
        ]
        
        for actor_data in actores_internos:
            actor = ActorInterno(**actor_data)
            db.session.add(actor)
        
        db.session.commit()
        print("✓ Actores internos creados")
        
        # 7. Crear tipos de problemática
        tipos_problematica = [
            {'nombre': 'Laboral'},
            {'nombre': 'Ambiental'},
            {'nombre': 'Territorial'},
            {'nombre': 'Servicios públicos'},
            {'nombre': 'Desarrollo social'},
            {'nombre': 'Seguridad'},
            {'nombre': 'Económica'},
            {'nombre': 'Política'},
            {'nombre': 'Otro'}
        ]
        
        for tipo_data in tipos_problematica:
            tipo = TipoProblematica(**tipo_data)
            db.session.add(tipo)
        
        db.session.commit()
        print("✓ Tipos de problemática creados")
        
        # 8. Crear grados de clasificación
        grados_clasificacion = [
            {'nombre': 'Bajo'},
            {'nombre': 'Medio'},
            {'nombre': 'Alto'},
            {'nombre': 'Crítico'}
        ]
        
        for grado_data in grados_clasificacion:
            grado = GradoClasificacion(**grado_data)
            db.session.add(grado)
        
        db.session.commit()
        print("✓ Grados de clasificación creados")
        
        # 9. Crear estatus generales
        estatus_list = [
            # Para estatus de reportes
            {'nombre': 'En proceso', 'tipo': 'reporte'},
            {'nombre': 'Atendido', 'tipo': 'reporte'},
            {'nombre': 'Cerrado', 'tipo': 'reporte'},
            {'nombre': 'Suspendido', 'tipo': 'reporte'},
            
            # Para cumplimiento de compromisos
            {'nombre': 'Sin iniciar', 'tipo': 'cumplimiento'},
            {'nombre': 'En proceso', 'tipo': 'cumplimiento'},
            {'nombre': 'Cumplido', 'tipo': 'cumplimiento'},
            {'nombre': 'Incumplido', 'tipo': 'cumplimiento'},
            
            # Para grado de probabilidad
            {'nombre': '25% En Atención', 'tipo': 'probabilidad'},
            {'nombre': '50% Autorizado', 'tipo': 'probabilidad'},
            {'nombre': '75% En Ejecución', 'tipo': 'probabilidad'},
            {'nombre': '100% Concluido', 'tipo': 'probabilidad'}
        ]
        
        for estatus_data in estatus_list:
            estatus = EstatusGeneral(**estatus_data)
            db.session.add(estatus)
        
        db.session.commit()
        print("✓ Estatus generales creados")
        
        # 10. Crear usuario administrador
        admin = Usuario(
            username='admin',
            email='admin@pemex.mx',
            nombre_completo='Administrador del Sistema',
            rol='Administrador'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Crear usuario capturista de ejemplo
        capturista = Usuario(
            username='capturista1',
            email='capturista1@pemex.mx',
            nombre_completo='Juan Pérez Capturista',
            rol='Capturista'
        )
        capturista.set_password('capturista123')
        db.session.add(capturista)
        
        db.session.commit()
        print("✓ Usuarios creados")
        print("\n=== DATOS DE ACCESO ===")
        print("Administrador:")
        print("  Usuario: admin")
        print("  Contraseña: admin123")
        print("\nCapturista:")
        print("  Usuario: capturista1")
        print("  Contraseña: capturista123")
        print("\n✓ Base de datos inicializada exitosamente")

if __name__ == '__main__':
    init_database()
