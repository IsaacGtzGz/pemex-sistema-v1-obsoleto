// Utilidades para el sistema PEMEX
const Utils = {
    // Cargar catálogos desde la API
    cargarCatalogos: {
        oficinasRegionales: function(selectElementId) {
            fetch('/api/catalogos/oficinas_regionales')
                .then(response => response.json())
                .then(data => {
                    const select = document.getElementById(selectElementId);
                    select.innerHTML = '<option value="">Seleccionar oficina regional</option>';
                    data.forEach(item => {
                        select.innerHTML += `<option value="${item.nombre}">${item.nombre} (${item.abreviacion})</option>`;
                    });
                });
        },
        
        tiposReporte: function(selectElementId) {
            fetch('/api/catalogos/tipos_reporte')
                .then(response => response.json())
                .then(data => {
                    const select = document.getElementById(selectElementId);
                    select.innerHTML = '<option value="">Seleccionar tipo de reporte</option>';
                    data.forEach(item => {
                        select.innerHTML += `<option value="${item.nombre}">${item.nombre}</option>`;
                    });
                });
        },
        
        entidadesFederativas: function(selectElementId) {
            fetch('/api/catalogos/entidades_federativas')
                .then(response => response.json())
                .then(data => {
                    const select = document.getElementById(selectElementId);
                    select.innerHTML = '<option value="">Seleccionar entidad federativa</option>';
                    data.forEach(item => {
                        select.innerHTML += `<option value="${item.nombre}" data-id="${item.id}">${item.nombre}</option>`;
                    });
                });
        },
        
        municipios: function(entidadId, selectElementId) {
            fetch(`/api/catalogos/municipios/${entidadId}`)
                .then(response => response.json())
                .then(data => {
                    const select = document.getElementById(selectElementId);
                    select.innerHTML = '<option value="">Seleccionar municipio</option>';
                    data.forEach(item => {
                        select.innerHTML += `<option value="${item.nombre}">${item.nombre}</option>`;
                    });
                });
        },
        
        actoresInternos: function(selectElementId) {
            fetch('/api/catalogos/actores_internos')
                .then(response => response.json())
                .then(data => {
                    const select = document.getElementById(selectElementId);
                    select.innerHTML = '<option value="">Seleccionar actor interno</option>';
                    data.forEach(item => {
                        select.innerHTML += `<option value="${item.nombre}">${item.nombre}</option>`;
                    });
                });
        },
        
        tiposAtencion: function(selectElementId) {
            fetch('/api/catalogos/tipos_atencion')
                .then(response => response.json())
                .then(data => {
                    const select = document.getElementById(selectElementId);
                    select.innerHTML = '<option value="">Seleccionar tipo de atención</option>';
                    data.forEach(item => {
                        select.innerHTML += `<option value="${item.nombre}">${item.nombre}</option>`;
                    });
                });
        }
    },

    // Mostrar notificaciones
    showNotification: function(message, type = 'info') {
        const alertClass = type === 'error' ? 'danger' : type;
        const icon = type === 'error' ? 'exclamation-triangle' : 
                    type === 'success' ? 'check-circle' : 'info-circle';
        
        const alertHtml = `
            <div class="alert alert-${alertClass} alert-dismissible fade show" role="alert">
                <i class="fas fa-${icon} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // Buscar contenedor de alertas o crear uno
        let alertContainer = document.querySelector('.alert-container');
        if (!alertContainer) {
            alertContainer = document.createElement('div');
            alertContainer.className = 'alert-container';
            document.querySelector('main').insertBefore(alertContainer, document.querySelector('main').firstChild);
        }
        
        alertContainer.innerHTML = alertHtml;
        
        // Auto-ocultar después de 5 segundos
        setTimeout(() => {
            const alert = alertContainer.querySelector('.alert');
            if (alert) {
                alert.remove();
            }
        }, 5000);
    },

    // Validar formulario
    validateForm: function(formId) {
        const form = document.getElementById(formId);
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });
        
        return isValid;
    },

    // Confirmar acción
    confirmAction: function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    },

    // Formatear fecha para input
    formatDateForInput: function(date) {
        return date.toISOString().split('T')[0];
    },

    // Generar folio automático (del lado cliente para vista previa)
    generarFolioPreview: function(tipoReporte, oficinaRegional) {
        const tiposAbrev = {
            'Acción Preventiva': 'AP',
            'Problemática Social': 'PS',
            'Contingencia': 'CON'
        };
        
        const oficinasAbrev = {
            'Oficina Regional Centro': 'ORC',
            'Oficina Regional Norte': 'ORN',
            'Oficina Regional Sur': 'ORS'
        };
        
        if (tipoReporte && oficinaRegional) {
            return `${oficinasAbrev[oficinaRegional]}-${tiposAbrev[tipoReporte]}-XXX`;
        }
        return '';
    },

    // Submits de formularios
    submitFormRegistroReporte: function(formId, esBorrador = false) {
        if (!this.validateForm(formId)) {
            this.showNotification('Por favor completa todos los campos requeridos', 'error');
            return;
        }
        
        const form = document.getElementById(formId);
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        data.guardar_borrador = esBorrador;
        
        fetch('/api/registro_reporte', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                this.showNotification(
                    `Reporte ${esBorrador ? 'guardado como borrador' : 'registrado'} exitosamente. Folio: ${result.folio}`, 
                    'success'
                );
                if (!esBorrador) {
                    form.reset();
                }
            } else {
                this.showNotification(result.error, 'error');
            }
        })
        .catch(error => {
            this.showNotification('Error al guardar el reporte', 'error');
        });
    },

    submitFormSeguimiento: function(formId) {
        if (!this.validateForm(formId)) {
            this.showNotification('Por favor completa todos los campos requeridos', 'error');
            return;
        }
        
        const form = document.getElementById(formId);
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        fetch('/api/seguimiento_compromiso', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                this.showNotification('Seguimiento guardado exitosamente', 'success');
                form.reset();
            } else {
                this.showNotification(result.error, 'error');
            }
        })
        .catch(error => {
            this.showNotification('Error al guardar el seguimiento', 'error');
        });
    },

    buscarReporte: function(folio, callback) {
        fetch(`/api/buscar_reporte/${folio}`)
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    callback(result.reporte);
                } else {
                    this.showNotification(result.error, 'error');
                }
            })
            .catch(error => {
                this.showNotification('Error al buscar el reporte', 'error');
            });
    }
};
