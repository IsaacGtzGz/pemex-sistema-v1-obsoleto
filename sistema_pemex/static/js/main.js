// JavaScript principal para Sistema PEMEX

// Configuración global
const PEMEX = {
    baseUrl: window.location.origin,
    version: '1.0.0',
    debug: true
};

// Utilidades generales
const Utils = {
    // Mostrar notificaciones
    showNotification: function(message, type = 'info', duration = 5000) {
        const alertClass = {
            'success': 'alert-success',
            'error': 'alert-danger',
            'warning': 'alert-warning',
            'info': 'alert-info'
        };
        
        const alert = $(`
            <div class="alert ${alertClass[type]} alert-dismissible fade show position-fixed" 
                 style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
                <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);
        
        $('body').append(alert);
        
        if (duration > 0) {
            setTimeout(() => {
                alert.alert('close');
            }, duration);
        }
    },
    
    // Confirmar acción
    confirmAction: function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    },
    
    // Formatear fecha
    formatDate: function(date, format = 'dd/mm/yyyy') {
        if (!date) return '';
        const d = new Date(date);
        const day = String(d.getDate()).padStart(2, '0');
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const year = d.getFullYear();
        
        return format.replace('dd', day).replace('mm', month).replace('yyyy', year);
    },
    
    // Validar formulario
    validateForm: function(formId) {
        const form = document.getElementById(formId);
        return form.checkValidity();
    },
    
    // Loading spinner
    showLoading: function(element) {
        const spinner = '<i class="fas fa-spinner fa-spin me-2"></i>Cargando...';
        if (typeof element === 'string') {
            $(`#${element}`).html(spinner);
        } else {
            $(element).html(spinner);
        }
    },
    
    // Ocultar loading
    hideLoading: function(element, originalText = '') {
        if (typeof element === 'string') {
            $(`#${element}`).html(originalText);
        } else {
            $(element).html(originalText);
        }
    }
};

// Formularios dinámicos
const FormHandler = {
    // Inicializar formularios
    init: function() {
        this.setupFieldDependencies();
        this.setupValidations();
        this.setupAutoSave();
    },
    
    // Configurar dependencias entre campos
    setupFieldDependencies: function() {
        // Oficina Regional -> Entidad Federativa
        $('#oficina_regional_id').on('change', function() {
            const oficinaId = $(this).val();
            FormHandler.loadEntidadesFederativas(oficinaId);
        });
        
        // Entidad Federativa -> Municipios
        $('#entidad_federativa_id').on('change', function() {
            const entidadId = $(this).val();
            FormHandler.loadMunicipios(entidadId);
        });
        
        // Tipo de Reporte -> Campos condicionales
        $('#tipo_reporte_id').on('change', function() {
            FormHandler.toggleConditionalFields();
        });
        
        // Tipo de Atención -> Campo "Otro"
        $('input[name="tipos_atencion"]').on('change', function() {
            FormHandler.toggleOtroTipoAtencion();
        });
        
        // Actor Interno -> Campo "Otro"
        $('#actor_interno_id').on('change', function() {
            FormHandler.toggleOtroActorInterno();
        });
        
        // Tipo de Problemática -> Campo "Otro"
        $('#tipo_problematica_id').on('change', function() {
            FormHandler.toggleOtroTipoProblematica();
        });
    },
    
    // Cargar entidades federativas
    loadEntidadesFederativas: function(oficinaId) {
        if (!oficinaId) {
            $('#entidad_federativa_id').html('<option value="">Selecciona una entidad</option>');
            $('#municipio_id').html('<option value="">Selecciona un municipio</option>');
            return;
        }
        
        Utils.showLoading('entidad_federativa_id');
        
        $.ajax({
            url: `/api/entidades-federativas/${oficinaId}`,
            type: 'GET',
            success: function(data) {
                let options = '<option value="">Selecciona una entidad</option>';
                data.forEach(entidad => {
                    options += `<option value="${entidad.id}">${entidad.nombre}</option>`;
                });
                $('#entidad_federativa_id').html(options);
                $('#municipio_id').html('<option value="">Selecciona un municipio</option>');
            },
            error: function() {
                Utils.showNotification('Error al cargar entidades federativas', 'error');
                $('#entidad_federativa_id').html('<option value="">Error al cargar</option>');
            }
        });
    },
    
    // Cargar municipios
    loadMunicipios: function(entidadId) {
        if (!entidadId) {
            $('#municipio_id').html('<option value="">Selecciona un municipio</option>');
            return;
        }
        
        Utils.showLoading('municipio_id');
        
        $.ajax({
            url: `/api/municipios/${entidadId}`,
            type: 'GET',
            success: function(data) {
                let options = '<option value="">Selecciona un municipio</option>';
                data.forEach(municipio => {
                    options += `<option value="${municipio.id}">${municipio.nombre}</option>`;
                });
                $('#municipio_id').html(options);
            },
            error: function() {
                Utils.showNotification('Error al cargar municipios', 'error');
                $('#municipio_id').html('<option value="">Error al cargar</option>');
            }
        });
    },
    
    // Mostrar/ocultar campos condicionales
    toggleConditionalFields: function() {
        const tipoReporte = $('#tipo_reporte_id option:selected').text();
        
        // Campos solo para PROBLEMÁTICA SOCIAL o CONFLICTO
        const camposProblematica = [
            '.campo-fecha-inicio',
            '.campo-tipo-problematica',
            '.campo-area-involucrada',
            '.campo-grado-clasificacion',
            '.campo-grado-probabilidad'
        ];
        
        // Campos solo para CONFLICTO
        const camposConflicto = [
            '.campo-fecha-lso',
            '.campo-dias-duracion'
        ];
        
        if (tipoReporte === 'Problemática Social' || tipoReporte === 'Conflicto') {
            camposProblematica.forEach(campo => {
                $(campo).show().addClass('show');
            });
        } else {
            camposProblematica.forEach(campo => {
                $(campo).hide().removeClass('show');
            });
        }
        
        if (tipoReporte === 'Conflicto') {
            camposConflicto.forEach(campo => {
                $(campo).show().addClass('show');
            });
        } else {
            camposConflicto.forEach(campo => {
                $(campo).hide().removeClass('show');
            });
        }
    },
    
    // Mostrar/ocultar campo "Otro tipo de atención"
    toggleOtroTipoAtencion: function() {
        const otroSeleccionado = $('input[name="tipos_atencion"][value="otro"]').is(':checked');
        if (otroSeleccionado) {
            $('.campo-otro-tipo-atencion').show().addClass('show');
            $('#otro_tipo_atencion').prop('required', true);
        } else {
            $('.campo-otro-tipo-atencion').hide().removeClass('show');
            $('#otro_tipo_atencion').prop('required', false);
        }
    },
    
    // Mostrar/ocultar campo "Otro actor interno"
    toggleOtroActorInterno: function() {
        const actorTexto = $('#actor_interno_id option:selected').text();
        if (actorTexto === 'Otro') {
            $('.campo-otro-actor-interno').show().addClass('show');
            $('#otro_actor_interno').prop('required', true);
        } else {
            $('.campo-otro-actor-interno').hide().removeClass('show');
            $('#otro_actor_interno').prop('required', false).val('N/A');
        }
    },
    
    // Mostrar/ocultar campo "Otro tipo de problemática"
    toggleOtroTipoProblematica: function() {
        const tipoTexto = $('#tipo_problematica_id option:selected').text();
        if (tipoTexto === 'Otro') {
            $('.campo-otro-problematica').show().addClass('show');
            $('#otro_tipo_problematica').prop('required', true);
        } else {
            $('.campo-otro-problematica').hide().removeClass('show');
            $('#otro_tipo_problematica').prop('required', false).val('N/A');
        }
    },
    
    // Validaciones personalizadas
    setupValidations: function() {
        // Validar fechas
        $('input[type="date"]').on('change', function() {
            FormHandler.validateDate(this);
        });
        
        // Validar campos requeridos
        $('.required').on('blur', function() {
            FormHandler.validateRequired(this);
        });
    },
    
    // Validar fecha
    validateDate: function(element) {
        const date = new Date(element.value);
        const today = new Date();
        const fieldName = element.name;
        
        if (fieldName === 'fecha_reporte' && date > today) {
            Utils.showNotification('La fecha de reporte no puede ser futura', 'warning');
            element.classList.add('field-error');
            return false;
        }
        
        element.classList.remove('field-error');
        element.classList.add('field-success');
        return true;
    },
    
    // Validar campo requerido
    validateRequired: function(element) {
        if (!element.value.trim()) {
            element.classList.add('field-error');
            return false;
        }
        
        element.classList.remove('field-error');
        element.classList.add('field-success');
        return true;
    },
    
    // Auto-guardado
    setupAutoSave: function() {
        if ($('#auto-save').length) {
            setInterval(() => {
                FormHandler.autoSave();
            }, 60000); // Cada minuto
        }
    },
    
    // Función de auto-guardado
    autoSave: function() {
        const formData = new FormData($('#main-form')[0]);
        
        $.ajax({
            url: '/api/auto-save',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function() {
                Utils.showNotification('Borrador guardado automáticamente', 'info', 2000);
            },
            error: function() {
                console.log('Error en auto-guardado');
            }
        });
    }
};

// Tablas dinámicas
const TableHandler = {
    init: function() {
        this.setupDataTables();
        this.setupFilters();
    },
    
    setupDataTables: function() {
        if ($.fn.DataTable) {
            $('.data-table').DataTable({
                language: {
                    url: 'https://cdn.datatables.net/plug-ins/1.11.5/i18n/es-ES.json'
                },
                responsive: true,
                pageLength: 25,
                dom: 'Bfrtip',
                buttons: [
                    'copy', 'csv', 'excel', 'pdf', 'print'
                ]
            });
        }
    },
    
    setupFilters: function() {
        $('.filter-select').on('change', function() {
            TableHandler.applyFilters();
        });
    },
    
    applyFilters: function() {
        // Implementar filtros personalizados
    }
};

// Inicialización cuando el documento esté listo
$(document).ready(function() {
    // Inicializar componentes
    FormHandler.init();
    TableHandler.init();
    
    // Configurar tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
    
    // Configurar modales
    $('.modal').on('hidden.bs.modal', function() {
        $(this).find('form')[0]?.reset();
    });
    
    // Configurar confirmaciones
    $('.confirm-action').on('click', function(e) {
        e.preventDefault();
        const message = $(this).data('confirm') || '¿Estás seguro de realizar esta acción?';
        const href = $(this).attr('href');
        
        Utils.confirmAction(message, function() {
            window.location.href = href;
        });
    });
    
    // Debug info
    if (PEMEX.debug) {
        console.log('Sistema PEMEX v' + PEMEX.version + ' inicializado correctamente');
    }
});

// Exportar para uso global
window.PEMEX = PEMEX;
window.Utils = Utils;
window.FormHandler = FormHandler;
window.TableHandler = TableHandler;
