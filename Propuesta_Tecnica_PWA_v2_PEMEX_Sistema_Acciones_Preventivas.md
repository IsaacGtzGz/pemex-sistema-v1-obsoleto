# PROPUESTA TÉCNICA PWA v2.0

## Sistema Web para Registro y Seguimiento de Acciones Preventivas y Problemática Social - PEMEX

---

**Elaborado por:** Isaac Gutiérrez Gómez  
**Fecha:** 15 de septiembre de 2025  
**Versión:** 2.0 (Arquitectura PWA Modernizada)

---

## RESUMEN EJECUTIVO

Esta propuesta presenta el desarrollo de un **Sistema Web PWA v2.0** para modernizar y digitalizar completamente el proceso de captura, consulta y seguimiento de reportes de acciones preventivas y problemática social en PEMEX, eliminando definitivamente el uso de Excel y migrando a una plataforma web centralizada de clase empresarial.

### Valor Agregado v2.0

- **Arquitectura PWA moderna** con funcionalidad offline
- **Stack tecnológico empresarial** (Next.js 14, TypeScript, PostgreSQL)
- **Seguridad robusta** con autenticación JWT y encriptación avanzada
- **Testing automatizado** y CI/CD para calidad garantizada
- **Escalabilidad empresarial** para crecimiento futuro

---

## 1. OBJETIVOS Y ALCANCE

### 1.1 Objetivo Principal

Desarrollar una **Progressive Web App (PWA)** que digitalice completamente el proceso manual de Excel, proporcionando una plataforma web centralizada, multiusuario, con control de acceso granular y validaciones robustas de negocio.

### 1.2 Alcance Funcional Completo

#### **FORMULARIOS PRINCIPALES**

1. **Registro de Reporte de Acciones Preventivas y Problemática Social** (44 campos desde columna A hasta CI)
2. **Seguimiento de Compromisos y/o Acuerdos** (16 campos desde columna CK hasta DE)

#### **GESTIÓN DE USUARIOS Y ROLES**

- **Administrador:** Gestión completa de usuarios y acceso total al sistema
- **Capturista:** Registro y seguimiento de reportes con permisos específicos
- **Autenticación segura** con políticas de contraseñas robustas

#### **FUNCIONALIDADES AVANZADAS**

- **Exportación inteligente** a Excel/CSV con formato personalizado
- **Validaciones estrictas** según reglas de negocio específicas de PEMEX
- **Catálogos dinámicos** (CAT 1-9) con dependencias automáticas
- **Campos editables controlados** con historial de cambios
- **Notificaciones contextuales** y mensajes de ayuda inteligentes
- **Acceso concurrente controlado** para prevenir conflictos de edición

---

## 2. ARQUITECTURA TÉCNICA PWA v2.0

### 2.1 Stack Tecnológico Modernizado

| Componente        | Tecnología                  | Justificación                                 |
| ----------------- | --------------------------- | --------------------------------------------- |
| **Frontend**      | Next.js 14 + TypeScript     | PWA nativa, SSR/SSG, performance superior     |
| **UI/UX**         | Tailwind CSS + Shadcn/UI    | Diseño moderno, responsive, accesible         |
| **Backend**       | Next.js API Routes + tRPC   | Type-safety completo, desarrollo ágil         |
| **Base de Datos** | PostgreSQL + Prisma ORM     | Robustez empresarial, migraciones automáticas |
| **Autenticación** | NextAuth.js + JWT           | Seguridad estándar industria                  |
| **Testing**       | Jest + Playwright + Cypress | Cobertura completa (unit, integration, e2e)   |
| **CI/CD**         | GitHub Actions              | Deployment automático, calidad garantizada    |
| **Hosting**       | Vercel/Railway + Supabase   | Escalabilidad global, monitoreo avanzado      |

### 2.2 Características PWA

- ✅ **Funcionalidad offline** para zonas de conectividad limitada
- ✅ **Instalación nativa** en dispositivos móviles y desktop
- ✅ **Notificaciones push** para alertas importantes
- ✅ **Sincronización automática** cuando se restaura conectividad
- ✅ **Performance optimizada** con carga instantánea

### 2.3 Seguridad Empresarial

- 🔐 **Encriptación AES-256** para datos sensibles
- 🔐 **Autenticación multifactor** opcional
- 🔐 **Auditoría completa** de acciones de usuario
- 🔐 **Protección OWASP Top 10** implementada
- 🔐 **Backup automático** y recuperación de desastres

---

## 3. ANÁLISIS FUNCIONAL DETALLADO

### 3.1 Formulario 1: Registro de Reporte (Columnas A-CI)

#### **CAMPOS AUTOMÁTICOS Y CALCULADOS**

- **A - Número de registro:** ID autogenerado, no editable
- **B - Responsable captura:** Usuario logueado automáticamente
- **D - Año de reporte:** Año actual automático
- **E - Folio:** Formato calculado `[Oficina]-[Tipo]-[Consecutivo]`
- **S - Días de duración:** Cálculo automático entre fechas J y R

#### **CATÁLOGOS IMPLEMENTADOS (CAT 1-9)**

| CAT       | Campo                    | Funcionalidad                     |
| --------- | ------------------------ | --------------------------------- |
| **CAT 1** | C - Oficina Regional     | 5 opciones con abreviaturas       |
| **CAT 2** | F - Tipo de Reporte      | 3 tipos con lógica condicional    |
| **CAT 3** | H - Entidad Federativa   | Filtrado por Oficina Regional     |
| **CAT 4** | I - Municipio(s)         | Filtrado por Entidad seleccionada |
| **CAT 5** | O - Tipo de atención     | Checkbox múltiple + campo "OTRO"  |
| **CAT 6** | V - Actores Internos     | Lista única + campo "OTRO"        |
| **CAT 7** | AA - Tipo Problemática   | Solo para Problemática/Conflicto  |
| **CAT 8** | AD - Grado Clasificación | Solo para Problemática/Conflicto  |
| **CAT 9** | CH, CI, DA - Estatus     | Múltiples usos según contexto     |

#### **VALIDACIONES ESPECIALIZADAS**

**📅 Gestión Inteligente de Fechas:**

- **Columna G:** Calendario con restricción 1 mes atrás + editable
- **Columna J:** Solo visible para Problemática/Conflicto
- **Columna R:** Solo para Conflictos, calcula duración automáticamente

**🔍 Validaciones de Negocio:**

- **Columna K:** Debe responder 3 preguntas obligatorias:
  1. ¿En dónde y quiénes?
  2. ¿En qué le afecta o beneficia a PEMEX?
  3. ¿Qué quieren o por qué hay que apoyarles?

**📝 Campos con Numeración Automática:**

- **Columna Q:** Compromisos/Acuerdos con historial de edición
- **Columna U:** Representantes/Líderes enumerados
- **Columna X:** Actores Externos opcionales enumerados

#### **CAMPOS CONDICIONALES POR TIPO DE REPORTE**

| Campo                    | Acción Preventiva | Problemática Social | Conflicto    |
| ------------------------ | ----------------- | ------------------- | ------------ |
| J - Fecha Inicio         | ❌ No aplica      | ✅ Visible          | ✅ Visible   |
| R - Fecha LSO            | ❌ No aplica      | ❌ No aplica        | ✅ Visible   |
| S - Días Duración        | ❌ No aplica      | ❌ No aplica        | ✅ Calculado |
| AA - Tipo Problemática   | ❌ No aplica      | ✅ Visible          | ✅ Visible   |
| AC - Área Involucrada    | ❌ No aplica      | ✅ Visible          | ✅ Visible   |
| AD - Grado Clasificación | ❌ No aplica      | ✅ Visible          | ✅ Visible   |
| AE-CF - Comportamiento   | ❌ No aplica      | ✅ Visible          | ✅ Visible   |
| CI - Grado Probabilidad  | ❌ No aplica      | ✅ Visible          | ✅ Visible   |

### 3.2 Formulario 2: Seguimiento (Columnas CK-DE)

#### **GESTIÓN DE FOLIOS**

- **Buscador inteligente** por tipo de reporte y folio específico
- **Control de concurrencia:** Prevención de edición simultánea
- **Notificación de usuario activo** con datos de contacto
- **Filtros dinámicos** por tipo de reporte

#### **SEGUIMIENTO MENSUAL (CO-CZ)**

- **12 campos mensuales** con opciones:
  - 25% En Atención
  - 50% Autorizado
  - 75% En Ejecución
  - 100% Concluido
- **Lógica inteligente:** Al alcanzar 100%, meses posteriores se ocultan
- **Campo DA calculado** automáticamente según porcentajes

#### **CAMPOS ESPECIALIZADOS**

- **CL:** Numeración automática con fechas opcionales
- **CM:** Contador automático de elementos del campo CL
- **CN:** Validación según tipo de atención seleccionada

---

## 4. CAMPOS EDITABLES Y HISTORIAL

### 4.1 Campos Editables (Verde en Excel Original)

| Campo     | Descripción          | Funcionalidad                          |
| --------- | -------------------- | -------------------------------------- |
| **G**     | Fecha de Reporte     | Actualización semanal para conflictos  |
| **Q**     | Compromisos/Acuerdos | Adición de elementos numerados         |
| **AE-CF** | Comportamiento 2025  | Sistema de seguimiento mensual         |
| **CG**    | Descripción Estatus  | Fecha + descripción (campos separados) |
| **CH**    | Estatus Actual       | Actualización según evolución          |
| **CI**    | Grado Probabilidad   | Solo para Problemática/Conflicto       |
| **CL-DA** | Todo el Seguimiento  | Formulario completo editable           |

### 4.2 Control de Versiones

- **Historial completo** de cambios por campo
- **Timestamp y usuario** en cada modificación
- **Reversión de cambios** con justificación
- **Auditoría completa** para compliance

---

## 5. PROPUESTAS DE MEJORA UX/UI

### 5.1 Ayudas Contextuales

- **Tooltips inteligentes** en campos complejos
- **Guías paso a paso** para nuevos usuarios
- **Validación en tiempo real** con mensajes claros
- **Autocompletado inteligente** basado en municipios

### 5.2 Catálogos de Referencia

- **Descarga de Excel** con todos los catálogos
- **Búsqueda rápida** dentro de catálogos extensos
- **Vista previa** del CAT 8 (Clasificación) integrada
- **Sugerencias automáticas** para campos relacionados

### 5.3 Funcionalidades Avanzadas

- **Dashboard de métricas** para administradores
- **Reportes personalizados** con filtros avanzados
- **Notificaciones automáticas** para seguimientos pendientes
- **Exportación masiva** con plantillas personalizadas

---

## 6. PREGUNTAS PARA CLARIFICACIÓN

### 6.1 Campos con Dudas Identificadas

**🔴 CRÍTICO - Comportamiento Columnas AE-CF:**

- ¿Cómo funcionará exactamente el sistema de colores mencionado?
- ¿Se relaciona con el campo CG o son independientes?
- ¿Requiere input manual o es calculado automáticamente?

**🟡 IMPORTANTE - Formato de Fechas + Descripciones:**

- En el campo CG, ¿confirman separar fecha y descripción en campos independientes?
- ¿El formato de fecha debe ser DD/MM/YYYY consistentemente?

**🟡 IMPORTANTE - Campos USO EXCLUSIVO SPV (DB-DE):**

- ¿Podrían explicar la funcionalidad exacta de estos campos?
- ¿Qué tipo de datos deben capturar Inicio/Continua/Concluye?
- ¿Son años, fechas, o códigos específicos?

**🟠 VALIDACIÓN - Folios Consecutivos:**

- ¿Los números XXX del folio son consecutivos automáticos o manuales?
- ¿Reinician cada año o son consecutivos globales?

### 6.2 Inconsistencias en Excel de Ejemplo

- **Campos N/A llenados:** Varios campos marcados como "no aplica" tienen datos
- **Colores vs Texto:** Inconsistencia entre formato visual y datos
- **Fechas mixtas:** Algunos campos mezclan fechas con texto libre

---

## 7. ARQUITECTURA DE HOSTING Y BASE DE DATOS

### 7.1 Opciones de Infraestructura

#### **OPCIÓN A: Infraestructura PEMEX Existente**

Si PEMEX cuenta con infraestructura IT propia:

- **Integración** con sistemas existentes
- **Compliance** con políticas internas
- **Soporte técnico** coordinado con TI PEMEX

#### **OPCIÓN B: Solución en la Nube (Recomendada)**

Plataforma moderna y escalable:

| Componente        | Servicio     | Costo Estimado Mensual |
| ----------------- | ------------ | ---------------------- |
| **Hosting Web**   | Vercel Pro   | $20 USD                |
| **Base de Datos** | Supabase Pro | $25 USD                |
| **Monitoreo**     | Sentry       | $26 USD                |
| **Backup**        | Automated    | Incluido               |
| **CDN Global**    | Cloudflare   | Gratuito               |
| **TOTAL**         |              | **~$71 USD/mes**       |

#### **OPCIÓN C: Solución Híbrida**

- **Frontend:** Nube para acceso global
- **Backend/BD:** Servidores PEMEX para datos sensibles
- **Sincronización:** API segura entre ambos

### 7.2 Seguridad y Compliance

- **Encriptación end-to-end** de datos
- **Backup automático** diario con retención 1 año
- **Logs de auditoría** completos para compliance
- **Certificación SSL/TLS** incluida
- **Monitoreo 24/7** con alertas automáticas

---

## 8. METODOLOGÍA DE DESARROLLO

### 8.1 Fases de Implementación

#### **FASE 1: Fundación (Semanas 1-2)**

- ✅ Setup inicial de proyecto PWA
- ✅ Configuración de base de datos PostgreSQL
- ✅ Implementación de autenticación
- ✅ Diseño del sistema de catálogos

#### **FASE 2: Formulario Principal (Semanas 3-4)**

- ✅ Desarrollo del formulario de registro
- ✅ Implementación de validaciones de negocio
- ✅ Sistema de catálogos dependientes
- ✅ Campos calculados automáticos

#### **FASE 3: Seguimiento y Gestión (Semanas 5-6)**

- ✅ Formulario de seguimiento
- ✅ Control de concurrencia
- ✅ Historial de cambios
- ✅ Dashboard administrativo

#### **FASE 4: Características Avanzadas (Semanas 7-8)**

- ✅ Exportación a Excel/CSV
- ✅ Funcionalidad offline PWA
- ✅ Notificaciones push
- ✅ Optimización de performance

#### **FASE 5: Testing y Deployment (Semanas 9-10)**

- ✅ Testing automatizado completo
- ✅ UAT con usuarios PEMEX
- ✅ Deployment a producción
- ✅ Capacitación y documentación

### 8.2 Entregables por Fase

- **Código fuente** en repositorio privado
- **Documentación técnica** completa
- **Manual de usuario** interactivo
- **Guía de administración** del sistema
- **Video tutoriales** para capacitación

---

## 9. GESTIÓN DE USUARIOS Y CAPACITACIÓN

### 9.1 Propuesta de Gestión de Usuarios

En lugar del campo de texto libre "Responsable de captura", se propone:

**✅ CRUD Completo de Usuarios:**

- Nombre, Apellido Paterno, Apellido Materno
- Teléfono, Correo electrónico
- Oficina Regional asignada
- Rol (Administrador/Capturista)
- Estado activo/inactivo

**✅ Beneficios:**

- **Autocompletado** del responsable al login
- **Contacto directo** para resolución de conflictos
- **Trazabilidad** completa de acciones
- **Seguridad** mejorada vs texto libre

### 9.2 Capacitación Incluida

- **Video manual interactivo** de uso del sistema
- **Sesión de capacitación virtual** con equipo PEMEX
- **Documentación PDF** descargable
- **Soporte técnico** durante primeros 30 días

---

## 10. CRONOGRAMA Y ENTREGABLES

### 10.1 Timeline Detallado

| Semana   | Entregables                      | Milestone                    |
| -------- | -------------------------------- | ---------------------------- |
| **1-2**  | Arquitectura + Autenticación     | ✅ Base técnica              |
| **3-4**  | Formulario principal + Catálogos | ✅ Funcionalidad core        |
| **5-6**  | Seguimiento + Gestión            | ✅ Sistema completo          |
| **7-8**  | PWA + Exportación                | ✅ Características avanzadas |
| **9-10** | Testing + Deployment             | ✅ Producción                |

### 10.2 Validaciones por Milestone

- **Validación técnica** con TI PEMEX (si aplica)
- **Feedback funcional** con usuarios finales
- **Ajustes** según retroalimentación
- **Aprobación** antes de siguiente fase

---

## 11. CONSIDERACIONES ADICIONALES

### 11.1 Evolución Futura

- **API REST** preparada para integraciones
- **Módulos adicionales** fácilmente extensibles
- **Analytics** e inteligencia de negocio
- **Mobile app nativa** (roadmap futuro)

### 11.2 Mantenimiento y Soporte

- **Actualizaciones de seguridad** automáticas
- **Nuevas funcionalidades** bajo solicitud
- **Soporte técnico** definible según acuerdo
- **Documentación** mantenida actualizada

### 11.3 Migración de Datos

- **Importación** desde Excel existente
- **Validación** de integridad de datos
- **Respaldo** completo antes de migración
- **Rollback** disponible si es necesario

---

## 12. PROPUESTA ECONÓMICA Y CONTRACTUAL

### 12.1 Inversión en Desarrollo

_[A definir según alcance final confirmado post-clarificaciones]_

**Incluye:**

- ✅ Desarrollo completo según especificaciones
- ✅ Testing y validación exhaustiva
- ✅ Deployment inicial y configuración
- ✅ Capacitación del equipo
- ✅ Documentación completa
- ✅ Soporte inicial 30 días

### 12.2 Costos Operativos Mensuales

- **Hosting en nube:** ~$71 USD/mes
- **Mantenimiento básico:** A cotizar según necesidades
- **Soporte técnico:** Modalidades disponibles

### 12.3 Modalidades de Contratación

- **Desarrollo completo:** Pago por proyecto terminado
- **Fases iterativas:** Pagos por milestone alcanzado
- **Desarrollo + Mantenimiento:** Modalidad híbrida

---

## 13. SIGUIENTES PASOS

### 13.1 Inmediatos

1. **Clarificación** de dudas técnicas identificadas
2. **Validación** de propuestas de mejora UX/UI
3. **Definición** de modalidad de hosting preferida
4. **Confirmación** de timeline y presupuesto

### 13.2 Inicio de Proyecto

1. **Firma de acuerdo** de desarrollo
2. **Setup** de repositorio y ambiente desarrollo
3. **Kick-off meeting** con stakeholders PEMEX
4. **Inicio** de Fase 1 según cronograma

---

## CONCLUSIÓN

Esta propuesta PWA v2.0 representa un **salto cuántico** en la modernización de los procesos de PEMEX, eliminando completamente la dependencia de Excel y proporcionando una solución robusta, escalable y preparada para el futuro.

**Beneficios Clave:**

- 🚀 **Eficiencia operativa** dramaticamente mejorada
- 🔒 **Seguridad empresarial** de clase mundial
- 📱 **Acceso moderno** desde cualquier dispositivo
- 📊 **Inteligencia de datos** para mejores decisiones
- 🌐 **Escalabilidad** para crecimiento organizacional

La inversión en esta modernización posicionará a PEMEX a la vanguardia tecnológica en gestión de procesos sociales y preventivos, con un ROI medible en productividad, reducción de errores y mejora en toma de decisiones.

---

**Isaac Gutiérrez Gómez**  
_Desarrollador de Soluciones Empresariales_  
_[Contacto y credenciales según requerimiento]_
