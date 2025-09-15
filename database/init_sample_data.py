"""
🚨 ARCHIVO DE INICIALIZACIÓN SEGURO 🚨

Este archivo contiene SOLO ejemplos ficticios para desarrollo.
NO contiene credenciales reales de PEMEX.

IMPORTANTE: En producción, las credenciales se manejan via:
- Variables de entorno (.env)
- Sistemas de gestión de secretos
- Configuración segura del servidor
"""

from app import app, db
from models import Usuario, ReporteProbematica, AccionPreventiva
import os

def init_sample_data():
    """
    Inicializa datos de ejemplo FICTICIOS para desarrollo.
    
    🔒 NOTA DE SEGURIDAD:
    - Las contraseñas aquí son solo para desarrollo local
    - En producción se usan hash seguros y variables de entorno
    - Los emails @ejemplo.local NO son emails reales
    """
    
    with app.app_context():
        # Verificar si ya existen usuarios
        if Usuario.query.first():
            print("⚠️  Los usuarios ya existen. Saltando inicialización.")
            return
        
        print("🔄 Creando usuarios de ejemplo...")
        
        # Usuario administrador FICTICIO
        admin_usuario = Usuario(
            username='admin_demo',
            email='admin.demo@ejemplo.local',  # EMAIL FICTICIO
            nombre_completo='Administrador Demo',
            rol='Administrador'
        )
        # Contraseña temporal solo para demo local
        admin_usuario.set_password(os.getenv('ADMIN_DEMO_PASSWORD', 'cambiar_en_produccion'))
        db.session.add(admin_usuario)
        
        # Usuario capturista FICTICIO  
        capturista_usuario = Usuario(
            username='capturista_demo',
            email='capturista.demo@ejemplo.local',  # EMAIL FICTICIO
            nombre_completo='Capturista Demo',
            rol='Capturista'
        )
        # Contraseña temporal solo para demo local
        capturista_usuario.set_password(os.getenv('CAPTURISTA_DEMO_PASSWORD', 'cambiar_en_produccion'))
        db.session.add(capturista_usuario)
        
        try:
            db.session.commit()
            print("✅ Usuarios de demo creados exitosamente")
            print("\n" + "="*50)
            print("🔒 CREDENCIALES PARA DESARROLLO LOCAL:")
            print("="*50)
            print("👤 Admin Demo:")
            print("   Usuario: admin_demo")
            print("   Password: [Ver variable ADMIN_DEMO_PASSWORD]")
            print("")
            print("👤 Capturista Demo:")  
            print("   Usuario: capturista_demo")
            print("   Password: [Ver variable CAPTURISTA_DEMO_PASSWORD]")
            print("="*50)
            print("🚨 RECORDATORIO: Configurar .env para producción")
            print("="*50)
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creando usuarios: {e}")

def create_sample_reports():
    """
    Crea reportes de ejemplo para demo (datos ficticios)
    """
    print("📄 Creando reportes de ejemplo...")
    # Aquí irían reportes ficticios para demo
    # (sin datos reales de PEMEX)
    pass

if __name__ == '__main__':
    print("🚀 Inicializando base de datos con datos de ejemplo...")
    print("🔒 Modo: DESARROLLO (datos ficticios únicamente)")
    init_sample_data()
    create_sample_reports()
    print("✅ Inicialización completa")