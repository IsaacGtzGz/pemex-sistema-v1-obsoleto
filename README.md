# ⚠️ REPOSITORIO OBSOLETO - PEMEX SISTEMA v1.0

Este repositorio contiene la versión 1.0 del sistema PEMEX (**obsoleta**).

## 🔗 NUEVA VERSIÓN v2.0 PWA

**Repositorio activo:** [pemex-sistema-v2-pwa](https://github.com/IsaacGtzGz/pemex-sistema-v2-pwa)

### 🚀 Características v2.0:

- ✅ **Progressive Web App (PWA)** con funcionalidad offline
- ✅ **Next.js 14 + TypeScript** para desarrollo moderno
- ✅ **MySQL + Prisma ORM** (migrado desde PostgreSQL por familiaridad del equipo)
- ✅ **Arquitectura moderna y escalable** con monorepo
- ✅ **Sistema de folios anuales** (2024-001, 2025-001)
- ✅ **Autenticación JWT** robusta con NextAuth.js
- ✅ **Validaciones inteligentes** para campos AE-CF
- ✅ **Testing automatizado** completo

### 📋 Migración de Funcionalidades:

| Característica v1.0    | Estado v2.0     | Mejoras                                    |
| ---------------------- | --------------- | ------------------------------------------ |
| **Formularios Excel**  | ✅ Digitalizado | Web forms con validaciones inteligentes    |
| **Campos manuales**    | ✅ Automatizado | Cálculos automáticos y catálogos dinámicos |
| **Sin control acceso** | ✅ Implementado | Roles (Admin/Capturista) con JWT           |
| **Archivos locales**   | ✅ Base datos   | MySQL centralizada con Prisma ORM          |
| **Sin seguimiento**    | ✅ Auditoría    | Historial completo de cambios              |
| **Excel dependiente**  | ✅ Web nativa   | PWA instalable en cualquier dispositivo    |

### 🔄 Proceso de Migración:

- **✅ Código:** Reescrito completamente en v2.0 con arquitectura moderna
- **✅ Datos:** Herramientas de migración automática disponibles
- **✅ Funcionalidad:** Todas las características v1.0 + nuevas mejoras
- **✅ Documentación:** Propuesta técnica completa y guías de usuario

---

## 📚 Documentación Histórica v1.0

### Archivos Disponibles en este Repositorio:

- `sistema_pemex/` - Código fuente v1.0 (obsoleto)
- `database/` - Esquemas de base de datos v1.0
- `Propuesta_Tecnica_PWA_v2_PEMEX_Sistema_Acciones_Preventivas.md` - Propuesta técnica v2.0
- `Estrategia_Repositorio_v2_PWA.md` - Plan de migración
- `250515 Propuesta base para Ap y prob 2025 -V2_issac.xlsx` - Análisis funcional Excel

### ⚠️ Advertencia de Seguridad

**No usar este código en producción.** La versión v1.0 contiene vulnerabilidades conocidas y carece de las medidas de seguridad implementadas en v2.0.

---

## 🎯 Recomendaciones

### Para Desarrollo Nuevo:

👉 **Usar exclusivamente [pemex-sistema-v2-pwa](https://github.com/IsaacGtzGz/pemex-sistema-v2-pwa)**

### Para Consulta Histórica:

👉 **Este repositorio permanece disponible solo para referencia**

### Para Migración de Datos:

👉 **Contactar equipo de desarrollo para herramientas de migración**

---

## 📞 Soporte

**Isaac Gutiérrez Gómez**  
_Desarrollador de Soluciones Empresariales_

- 🐙 **GitHub:** [@IsaacGtzGz](https://github.com/IsaacGtzGz)
- 📧 **Email:** [Contacto disponible en nuevo repositorio]
- 💼 **LinkedIn:** [Perfil disponible en nuevo repositorio]

---

**Estado:** 🔒 **Archivado** (Solo consulta histórica)  
**Última actualización:** Diciembre 2024  
**Repositorio activo:** [pemex-sistema-v2-pwa](https://github.com/IsaacGtzGz/pemex-sistema-v2-pwa)

---

**© 2024 PEMEX - Sistema de Acciones Preventivas y Problemática Social**

## ⚠️ **IMPORTANTE: ESTE PROTOTIPO ESTÁ DISCONTINUADO**

Este repositorio contiene el **primer prototipo** del Sistema Web para Registro y Seguimiento de Acciones Preventivas y Problemática Social de PEMEX.

### 🔴 **Por qué se descontinuó:**

1. **Errores acumulados**: Múltiples inconsistencias en la base de datos
2. **Templates mal estructurados**: admin.html con errores de sintaxis
3. **Código difícil de mantener**: Funcionalidades incompletas e inconsistentes
4. **Arquitectura problemática**: Demasiados parches sobre parches

### 📋 **Lo que SÍ funcionaba:**

- ✅ Autenticación básica (login/logout)
- ✅ Modelos de base de datos (diseño conceptual correcto)
- ✅ Colores PEMEX oficiales implementados
- ✅ Responsive design básico
- ✅ Estructura Flask básica

### 🎯 **Nueva Arquitectura PWA v2.0:**

- ✅ **Propuesta técnica completa** generada ([PDF disponible](./Propuesta_Tecnica_PWA_v2_PEMEX_Sistema_Acciones_Preventivas.pdf))
- ✅ **Next.js 14 + TypeScript** como stack principal
- ✅ **PostgreSQL + Prisma ORM** para robustez empresarial
- ✅ **PWA completo** con funcionalidad offline
- ✅ **Testing automatizado** desde el inicio
- ✅ **Documentación exhaustiva** de requerimientos funcionales

---

## 🏗️ **Arquitectura del Prototipo v1.0**

### **Stack Tecnológico:**

- **Backend**: Flask 2.3.2 + SQLAlchemy
- **Base de datos**: MySQL 8.0
- **Frontend**: Bootstrap 5 + JavaScript vanilla
- **Autenticación**: Flask-Login
- **Formularios**: Flask-WTF

### **Estructura del Proyecto:**

```
sistema_pemex/
├── app.py              # Aplicación Flask principal
├── models.py           # Modelos SQLAlchemy
├── config.py           # Configuración
├── requirements.txt    # Dependencias Python
├── static/
│   ├── css/
│   │   ├── pemex-theme-new.css  # Tema PEMEX oficial
│   │   └── styles.css           # Estilos adicionales
│   └── js/
│       ├── pemex-utils.js       # Utilidades JavaScript
│       └── main.js              # Scripts principales
└── templates/
    ├── base.html
    ├── login.html
    ├── dashboard.html
    ├── admin_dashboard.html
    ├── registro_reporte.html
    ├── acciones.html
    ├── seguimiento_acuerdos.html
    ├── reportes.html
    └── admin.html           # ❌ ARCHIVO CON ERRORES
```

### **Problemas Identificados:**

#### 🔥 **Errores Críticos:**

- `admin.html`: Error de sintaxis Jinja2 - "unknown tag 'endblock'"
- Inconsistencias en la base de datos entre vistas
- DataTables se reinicializa incorrectamente
- Manejo de errores inconsistente

#### ⚠️ **Problemas de Diseño:**

- Templates no siguen un patrón consistente
- CSS mezclado entre múltiples archivos
- JavaScript no modularizado correctamente
- Validaciones del lado cliente incompletas

#### 🐛 **Problemas Funcionales:**

- Formularios sin validación robusta
- Reportes no generan correctamente
- Seguimiento de acuerdos incompleto
- Panel de administración no funcional

---

## 📊 **Lecciones Aprendidas**

### **✅ Qué hacer en el v2.0:**

1. **Desarrollo incremental** con validaciones en cada paso
2. **Tests automatizados** desde el primer commit
3. **Arquitectura PWA** para mejor experiencia de usuario
4. **Documentación continua** de cada funcionalidad
5. **Revisiones de código** antes de integrar cambios

### **❌ Qué NO repetir:**

1. Agregar funcionalidades sin probar las anteriores
2. Modificar templates sin validar sintaxis
3. Acumular errores sin resolverlos inmediatamente
4. Desarrollo sin plan arquitectónico claro

---

## 🚀 **Roadmap v2.0 (PWA)**

### **Fase 1: Fundación Sólida**

- [ ] Setup inicial con TypeScript + PWA
- [ ] Tests automatizados configurados
- [ ] CI/CD pipeline básico
- [ ] Documentación automatizada

### **Fase 2: Autenticación y Seguridad**

- [ ] Sistema de autenticación robusto
- [ ] Manejo de sesiones seguro
- [ ] Validaciones del lado servidor y cliente
- [ ] Logging y auditoría

### **Fase 3: Funcionalidades Core**

- [ ] Registro de reportes con validación completa
- [ ] Sistema de acciones preventivas
- [ ] Seguimiento de acuerdos robusto
- [ ] Panel de administración funcional

### **Fase 4: PWA y UX**

- [ ] Service Workers para offline
- [ ] Notificaciones push
- [ ] Instalación como app nativa
- [ ] Optimización de rendimiento

---

## 📞 **Contacto del Proyecto**

**Desarrollador**: GitHub Copilot  
**Cliente**: PEMEX - Dirección de Asuntos Sociales  
**Fecha**: Septiembre 2025  
**Estado**: PROTOTIPO DESCONTINUADO ❌

---

_"Un paso atrás para dar dos pasos adelante. La experiencia de este prototipo nos dará la sabiduría para crear un sistema robusto en v2.0"_
