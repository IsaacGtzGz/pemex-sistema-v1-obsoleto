/* ============================================
   UTILIDADES JAVASCRIPT PARA SISTEMA PEMEX
   ============================================ */

// Namespace global para utilidades
window.PemexUtils = window.PemexUtils || {};

// Utilidades para DataTables
PemexUtils.DataTables = {
  /**
   * Inicializa un DataTable de manera segura
   * @param {string} selector - Selector CSS de la tabla
   * @param {object} options - Opciones para DataTable
   */
  init: function(selector, options = {}) {
    const $table = $(selector);
    
    if ($table.length === 0) {
      console.warn(`Tabla no encontrada: ${selector}`);
      return null;
    }

    // Destruir DataTable existente si está inicializado
    if ($.fn.DataTable.isDataTable(selector)) {
      $table.DataTable().destroy();
    }

    // Configuración por defecto
    const defaultOptions = {
      language: {
        url: 'https://cdn.datatables.net/plug-ins/1.11.5/i18n/es-ES.json'
      },
      responsive: true,
      pageLength: 25,
      dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>' +
           '<"row"<"col-sm-12"tr>>' +
           '<"row"<"col-sm-12 col-md-5"i><"col-sm-12 col-md-7"p>>',
      columnDefs: [
        { targets: 'no-sort', orderable: false }
      ]
    };

    // Combinar opciones
    const finalOptions = $.extend(true, {}, defaultOptions, options);

    try {
      const dataTable = $table.DataTable(finalOptions);
      
      // Agregar eventos personalizados
      dataTable.on('draw', function() {
        PemexUtils.updateCounter(selector);
      });

      console.log(`DataTable inicializado exitosamente: ${selector}`);
      return dataTable;
    } catch (error) {
      console.error(`Error al inicializar DataTable ${selector}:`, error);
      return null;
    }
  },

  /**
   * Destruye un DataTable de manera segura
   * @param {string} selector - Selector CSS de la tabla
   */
  destroy: function(selector) {
    if ($.fn.DataTable.isDataTable(selector)) {
      $(selector).DataTable().destroy();
      console.log(`DataTable destruido: ${selector}`);
    }
  },

  /**
   * Reinicia un DataTable
   * @param {string} selector - Selector CSS de la tabla
   * @param {object} options - Nuevas opciones
   */
  reinit: function(selector, options = {}) {
    this.destroy(selector);
    return this.init(selector, options);
  }
};

// Utilidades generales
PemexUtils.updateCounter = function(selector) {
  const $table = $(selector);
  const info = $table.DataTable().page.info();
  const counterId = selector.replace('#tabla-', '#contador-');
  
  if ($(counterId).length > 0) {
    $(counterId).text(`${info.recordsDisplay} de ${info.recordsTotal} registros`);
  }
};

// Utilidades para notificaciones
PemexUtils.showNotification = function(message, type = 'info', duration = 3000) {
  // Crear contenedor de notificaciones si no existe
  if ($('#notification-container').length === 0) {
    $('body').append('<div id="notification-container" style="position: fixed; top: 20px; right: 20px; z-index: 9999;"></div>');
  }

  const alertClass = {
    'success': 'alert-success',
    'error': 'alert-danger',
    'warning': 'alert-warning',
    'info': 'alert-info'
  }[type] || 'alert-info';

  const iconClass = {
    'success': 'fa-check-circle',
    'error': 'fa-exclamation-triangle',
    'warning': 'fa-exclamation-triangle',
    'info': 'fa-info-circle'
  }[type] || 'fa-info-circle';

  const notificationId = 'notification-' + Date.now();
  const notification = `
    <div id="${notificationId}" class="alert ${alertClass} alert-dismissible fade show mb-2" role="alert" style="min-width: 300px;">
      <i class="fas ${iconClass} me-2"></i>
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
    </div>
  `;

  $('#notification-container').append(notification);

  // Auto cerrar después del tiempo especificado
  if (duration > 0) {
    setTimeout(() => {
      $(`#${notificationId}`).fadeOut(300, function() {
        $(this).remove();
      });
    }, duration);
  }
};

// Utilidades para formularios
PemexUtils.Form = {
  /**
   * Valida un formulario
   * @param {string} formSelector - Selector del formulario
   */
  validate: function(formSelector) {
    const form = document.querySelector(formSelector);
    if (!form) return false;
    
    return form.checkValidity();
  },

  /**
   * Serializa un formulario a objeto
   * @param {string} formSelector - Selector del formulario
   */
  toObject: function(formSelector) {
    const formData = new FormData(document.querySelector(formSelector));
    const object = {};
    formData.forEach((value, key) => {
      object[key] = value;
    });
    return object;
  },

  /**
   * Resetea un formulario y limpia validaciones
   * @param {string} formSelector - Selector del formulario
   */
  reset: function(formSelector) {
    const form = document.querySelector(formSelector);
    if (form) {
      form.reset();
      form.classList.remove('was-validated');
      
      // Limpiar mensajes de error personalizados
      $(formSelector + ' .invalid-feedback').remove();
      $(formSelector + ' .is-invalid').removeClass('is-invalid');
    }
  }
};

// Utilidades para modales
PemexUtils.Modal = {
  /**
   * Abre un modal
   * @param {string} modalId - ID del modal
   */
  show: function(modalId) {
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    modal.show();
  },

  /**
   * Cierra un modal
   * @param {string} modalId - ID del modal
   */
  hide: function(modalId) {
    const modalElement = document.getElementById(modalId);
    const modal = bootstrap.Modal.getInstance(modalElement);
    if (modal) {
      modal.hide();
    }
  }
};

// Inicialización automática cuando el DOM esté listo
$(document).ready(function() {
  // Inicializar tooltips de Bootstrap
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Inicializar popovers de Bootstrap
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });

  console.log('PemexUtils inicializado correctamente');
});
