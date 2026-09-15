document.addEventListener('DOMContentLoaded', function() {
    // ===================== CONFIGURACIÓN =====================
    const tableBody = document.getElementById('body-venta');
    const addButton = document.getElementById('add-product');
    const totalGeneralElement = document.getElementById('total-general');
    const totalGeneralBs = document.getElementById('total-general-bs');
    const clienteSearch = document.getElementById('cliente-search');
    const clienteSelect = document.getElementById('cliente');
    const clienteSuggestions = document.getElementById('cliente-suggestions');
    const clienteSeleccionado = document.getElementById('cliente-seleccionado');
    const clienteNombreSeleccionado = document.getElementById('cliente-nombre-seleccionado');

    // Elementos de pago
    const metodoPagoRadios = document.querySelectorAll('.metodo-pago');
    const efectivoFields = document.getElementById('efectivo-fields');
    const creditoFields = document.getElementById('credito-fields');
    const montoRecibido = document.getElementById('monto-recibido');
    const montoCambio = document.getElementById('monto-cambio');
    const descuentoInput = document.getElementById('descuento-input');

    // Elementos de desglose
    const desgloseSubtotal = document.getElementById('desglose-subtotal');
    const desgloseIva = document.getElementById('desglose-iva');
    const desgloseTotalIva = document.getElementById('desglose-total-iva');
    const desgloseTotalDescuento = document.getElementById('desglose-total-descuento');
    const totalBs = document.getElementById('total-bs');
    const tasaBcv = document.getElementById('tasa-bcv');

    // Buscador de productos
    const buscadorProductos = document.getElementById('buscador-productos');
    const productoSuggestions = document.getElementById('producto-suggestions');
    const btnScanBarcode = document.getElementById('btn-scan-barcode');

    // ===================== TASA DE CAMBIO (BCV) =====================
    let tasaCambio = 0;

    function obtenerTasaBCV() {
        try {
            const scriptData = document.getElementById('tasa-dolar-data');
            if (scriptData) {
                // JSON.parse convierte la etiqueta directamente al número/objeto enviado por Django
                tasaCambio = parseFloat(JSON.parse(scriptData.textContent)) || 36.50;
            } else {
                tasaCambio = 36.50;
            }
            actualizarTasas();
        } catch (error) {
            console.error('Error al parsear la tasa BCV:', error);
            tasaCambio = 36.50; // Valor de respaldo (fallback)
            actualizarTasas();
        }
    }

    function actualizarTasas() {
        document.getElementById('tasa-usd-header').textContent = '1.00';
        document.getElementById('tasa-bs-header').textContent = tasaCambio.toFixed(2);
        
        const tasaBcv = document.getElementById('tasaBcv'); // Asegúrate de seleccionar el elemento si no existe globalmente
        if (tasaBcv) {
            tasaBcv.textContent = `1 USD = ${tasaCambio.toFixed(2)} Bs`;
        }
        
        calcularTotalesGenerales();
    }

    // ===================== CLIENTE - BÚSQUEDA =====================
    const clientesData = Array.from(clienteSelect.options).map(opt => ({
        id: opt.value,
        nombre: opt.getAttribute('data-nombre') || opt.textContent,
        documento: opt.getAttribute('data-documento') || ''
    })).filter(c => c.id);

    clienteSearch.addEventListener('input', function() {
        const query = this.value.toLowerCase().trim();
        if (query.length < 1) {
            clienteSuggestions.style.display = 'none';
            return;
        }

        const filtered = clientesData.filter(c => 
            c.nombre.toLowerCase().includes(query) || 
            c.documento.includes(query)
        );

        if (filtered.length === 0) {
            clienteSuggestions.innerHTML = `
                <div class="list-group-item text-muted text-center">
                    <i class="fas fa-user-slash me-1"></i> No se encontraron clientes
                </div>
            `;
            clienteSuggestions.style.display = 'block';
            return;
        }

        clienteSuggestions.innerHTML = filtered.map(c => `
            <button type="button" class="list-group-item list-group-item-action" data-id="${c.id}">
                <div class="d-flex justify-content-between align-items-center">
                    <span><i class="fas fa-user me-2"></i> ${c.nombre}</span>
                    <span class="badge bg-secondary">${c.documento}</span>
                </div>
            </button>
        `).join('');

        clienteSuggestions.style.display = 'block';

        clienteSuggestions.querySelectorAll('button').forEach(btn => {
            btn.addEventListener('click', function() {
                const id = this.dataset.id;
                const cliente = clientesData.find(c => c.id === id);
                if (cliente) {
                    clienteSelect.value = id;
                    clienteSearch.value = cliente.nombre;
                    clienteNombreSeleccionado.textContent = cliente.nombre;
                    clienteSeleccionado.classList.remove('d-none');
                    clienteSuggestions.style.display = 'none';
                }
            });
        });
    });

    document.addEventListener('click', function(e) {
        if (!clienteSearch.contains(e.target) && !clienteSuggestions.contains(e.target)) {
            clienteSuggestions.style.display = 'none';
        }
    });

    // ===================== BUSCADOR AVANZADO DE PRODUCTOS =====================
    const productosData = [];
    document.querySelectorAll('.select-producto option').forEach(opt => {
        if (opt.value) {
            productosData.push({
                id: opt.value,
                nombre: opt.textContent.trim(),
                precio: parseFloat(opt.getAttribute('data-precio')) || 0,
                stock: parseInt(opt.getAttribute('data-stock')) || 0,
                codigo: opt.getAttribute('data-codigo') || ''
            });
        }
    });

    buscadorProductos.addEventListener('input', function() {
        const query = this.value.toLowerCase().trim();
        if (query.length < 1) {
            productoSuggestions.style.display = 'none';
            return;
        }

        const filtered = productosData.filter(p => 
            p.nombre.toLowerCase().includes(query) || 
            p.codigo.includes(query)
        ).slice(0, 10);

        if (filtered.length === 0) {
            productoSuggestions.innerHTML = `
                <div class="list-group-item text-muted text-center">
                    <i class="fas fa-box-open me-1"></i> No se encontraron productos
                </div>
            `;
            productoSuggestions.style.display = 'block';
            return;
        }

        productoSuggestions.innerHTML = filtered.map(p => `
            <button type="button" class="list-group-item list-group-item-action" data-id="${p.id}">
                <div class="d-flex justify-content-between align-items-center">
                    <span><strong>${p.nombre}</strong></span>
                    <span class="badge bg-success">$ ${p.precio.toFixed(2)}</span>
                </div>
                <small class="text-muted">Stock: ${p.stock} | Código: ${p.codigo || 'N/A'}</small>
            </button>
        `).join('');

        productoSuggestions.style.display = 'block';

        productoSuggestions.querySelectorAll('button').forEach(btn => {
            btn.addEventListener('click', function() {
                const id = this.dataset.id;
                // Buscar la primera fila vacía o agregar nueva
                let targetRow = null;
                document.querySelectorAll('.fila-producto').forEach(row => {
                    const select = row.querySelector('.select-producto');
                    if (!select.value) {
                        targetRow = row;
                    }
                });
                
                if (!targetRow) {
                    // Agregar nueva fila
                    addButton.click();
                    targetRow = document.querySelector('.fila-producto:last-child');
                }
                
                const select = targetRow.querySelector('.select-producto');
                select.value = id;
                const event = new Event('change');
                select.dispatchEvent(event);
                
                buscadorProductos.value = '';
                productoSuggestions.style.display = 'none';
            });
        });
    });

    // Escaneo de código de barras (simulado)
    btnScanBarcode.addEventListener('click', function() {
        // En producción, esto activaría la cámara o lector de códigos
        alert('📷 Escaneo de código de barras activado.\nPor favor, acerca el código a la cámara.');
        // Simulación: buscar por código
        const codigoSimulado = prompt('Ingresa el código de barras (simulación):');
        if (codigoSimulado) {
            buscadorProductos.value = codigoSimulado;
            const event = new Event('input');
            buscadorProductos.dispatchEvent(event);
        }
    });

    document.addEventListener('click', function(e) {
        if (!buscadorProductos.contains(e.target) && !productoSuggestions.contains(e.target)) {
            productoSuggestions.style.display = 'none';
        }
    });

    // ===================== CÁLCULOS =====================
    function calcularSubtotalYTotal(row) {
        const select = row.querySelector('.select-producto');
        const inputCantidad = row.querySelector('.input-cantidad');
        const precioVisual = row.querySelector('.precio-visual');
        const subtotalVisual = row.querySelector('.subtotal-visual');
        const stockIndicator = row.querySelector('.stock-indicator');

        const selectedOption = select.options[select.selectedIndex];
        const precio = parseFloat(selectedOption.getAttribute('data-precio')) || 0;
        const stock = parseInt(selectedOption.getAttribute('data-stock')) || 0;
        let cantidad = parseInt(inputCantidad.value) || 0;

        if (stock > 0 && cantidad > stock) {
            inputCantidad.value = stock;
            cantidad = stock;
            stockIndicator.className = 'badge stock-indicator bg-warning rounded-pill';
            stockIndicator.textContent = 'Máximo: ' + stock;
        } else if (stock === 0) {
            stockIndicator.className = 'badge stock-indicator bg-danger rounded-pill';
            stockIndicator.textContent = 'Agotado';
        } else {
            stockIndicator.className = 'badge stock-indicator bg-success rounded-pill';
            stockIndicator.textContent = `Stock: ${stock}`;
        }

        precioVisual.value = `$ ${precio.toFixed(2)}`;
        const subtotal = precio * cantidad;
        subtotalVisual.value = `$ ${subtotal.toFixed(2)}`;

        calcularTotalesGenerales();
    }

    function calcularTotalesGenerales() {
        let total = 0;
        let totalItems = 0;
        let totalProductos = 0;

        document.querySelectorAll('.fila-producto').forEach(row => {
            const select = row.querySelector('.select-producto');
            const inputCantidad = row.querySelector('.input-cantidad');
            const selectedOption = select.options[select.selectedIndex];
            const precio = parseFloat(selectedOption.getAttribute('data-precio')) || 0;
            const cantidad = parseInt(inputCantidad.value) || 0;

            if (select.value) {
                totalProductos++;
                totalItems += cantidad;
                total += precio * cantidad;
            }
        });

        // Aplicar descuento
        const descuento = parseFloat(descuentoInput.value) || 0;
        const subtotal = total;
        const iva = subtotal * 0.16;
        const totalConIva = subtotal + iva;
        const totalConDescuento = totalConIva - descuento;

        // Actualizar desglose
        desgloseSubtotal.textContent = `$ ${subtotal.toFixed(2)}`;
        desgloseIva.textContent = `$ ${iva.toFixed(2)}`;
        desgloseTotalIva.textContent = `$ ${totalConIva.toFixed(2)}`;
        desgloseTotalDescuento.textContent = `$ ${totalConDescuento.toFixed(2)}`;

        // Actualizar totales
        const totalFinal = Math.max(totalConDescuento, 0);
        totalGeneralElement.textContent = `$ ${totalFinal.toFixed(2)}`;
        
        // Conversión a Bs
        const totalBsValue = totalFinal * tasaCambio;
        totalGeneralBs.textContent = `Bs ${totalBsValue.toFixed(2)}`;
        totalBs.textContent = `Bs ${totalBsValue.toFixed(2)}`;

        //convertir a dolares
        const totalDolares = totalFinal;
        document.getElementById('total-dolares').textContent = `$ ${totalDolares.toFixed(2)}`;

        document.getElementById('resumen-productos').textContent = totalProductos;
        document.getElementById('resumen-items').textContent = totalItems;
        document.getElementById('resumen-subtotal').textContent = `$ ${subtotal.toFixed(2)}`;
        document.getElementById('product-count').textContent = `${totalProductos} productos`;

        // Calcular cambio si es efectivo
        calcularCambio(totalFinal);
    }

    function calcularCambio(total) {
        const monto = parseFloat(montoRecibido.value) || 0;
        if (monto > 0 && monto >= total) {
            const cambio = monto - total;
            montoCambio.value = cambio.toFixed(2);
        } else if (monto > 0 && monto < total) {
            montoCambio.value = `Faltan $ ${(total - monto).toFixed(2)}`;
        } else {
            montoCambio.value = '0.00';
        }
    }

    // ===================== MÉTODOS DE PAGO =====================
    metodoPagoRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'efectivo') {
                efectivoFields.classList.remove('d-none');
                creditoFields.classList.add('d-none');
            } else if (this.value === 'credito') {
                efectivoFields.classList.add('d-none');
                creditoFields.classList.remove('d-none');
            } else {
                efectivoFields.classList.add('d-none');
                creditoFields.classList.add('d-none');
            }
        });
    });

    montoRecibido.addEventListener('input', function() {
        calcularTotalesGenerales();
    });

    descuentoInput.addEventListener('input', function() {
        calcularTotalesGenerales();
    });

    // ===================== EVENTOS DE TABLA =====================
    tableBody.addEventListener('change', function(e) {
        if (e.target.classList.contains('select-producto')) {
            const row = e.target.closest('tr');
            const option = e.target.options[e.target.selectedIndex];
            const stock = parseInt(option.getAttribute('data-stock')) || 0;
            if (stock === 0) {
                alert('Este producto no tiene stock disponible.');
                e.target.value = '';
            }
            calcularSubtotalYTotal(row);
        }
        if (e.target.classList.contains('input-cantidad')) {
            const row = e.target.closest('tr');
            calcularSubtotalYTotal(row);
        }
    });

    tableBody.addEventListener('input', function(e) {
        if (e.target.classList.contains('input-cantidad')) {
            const row = e.target.closest('tr');
            calcularSubtotalYTotal(row);
        }
    });

    // ===================== AGREGAR PRODUCTO =====================
    addButton.addEventListener('click', function() {
        const firstRow = document.querySelector('.fila-producto');
        const newRow = firstRow.cloneNode(true);
        
        newRow.querySelector('.select-producto').selectedIndex = 0;
        newRow.querySelector('.input-cantidad').value = 1;
        newRow.querySelector('.precio-visual').value = '$ 0.00';
        newRow.querySelector('.subtotal-visual').value = '$ 0.00';
        newRow.querySelector('.stock-indicator').className = 'badge stock-indicator bg-success rounded-pill';
        newRow.querySelector('.stock-indicator').textContent = 'Disponible';

        newRow.style.opacity = '0';
        newRow.style.transform = 'translateY(-10px)';
        
        tableBody.appendChild(newRow);
        
        requestAnimationFrame(() => {
            newRow.style.transition = 'all 0.3s ease';
            newRow.style.opacity = '1';
            newRow.style.transform = 'translateY(0)';
        });

        calcularTotalesGenerales();
    });

    // ===================== ELIMINAR PRODUCTO =====================
    tableBody.addEventListener('click', function(e) {
        const removeBtn = e.target.closest('.remove-row');
        if (removeBtn) {
            const rows = document.querySelectorAll('.fila-producto');
            if (rows.length > 1) {
                const row = removeBtn.closest('tr');
                row.style.transition = 'all 0.3s ease';
                row.style.opacity = '0';
                row.style.transform = 'translateX(20px)';
                setTimeout(() => {
                    row.remove();
                    calcularTotalesGenerales();
                }, 300);
            } else {
                alert('La factura debe tener al menos un producto.');
            }
        }
    });

    // ===================== VALIDACIÓN ANTES DE ENVIAR =====================
    document.getElementById('form-venta').addEventListener('submit', function(e) {
        const clienteValue = clienteSelect.value;
        if (!clienteValue) {
            e.preventDefault();
            alert('Por favor, selecciona un cliente.');
            clienteSearch.focus();
            clienteSearch.classList.add('is-invalid');
            return;
        }

        const productos = document.querySelectorAll('.fila-producto');
        let isValid = true;
        productos.forEach(row => {
            const select = row.querySelector('.select-producto');
            if (!select.value) {
                isValid = false;
            }
        });

        if (!isValid) {
            e.preventDefault();
            alert('Por favor, selecciona un producto para cada fila.');
        }

        // Validar método de pago
        const metodoSeleccionado = document.querySelector('.metodo-pago:checked');
        if (metodoSeleccionado.value === 'efectivo') {
            const monto = parseFloat(montoRecibido.value) || 0;
            const total = parseFloat(totalGeneralElement.textContent.replace('$ ', '')) || 0;
            if (monto < total) {
                e.preventDefault();
                alert('El monto recibido es menor al total de la venta.');
            }
        }
    });

    // ===================== INICIALIZACIÓN =====================
    obtenerTasaBCV();
    
    document.querySelectorAll('.fila-producto').forEach(row => {
        calcularSubtotalYTotal(row);
    });

    // ===================== VALIDACIÓN ANTES DE ENVIAR =====================
document.getElementById('form-venta').addEventListener('submit', function(e) {
    const clienteValue = clienteSelect.value;
    if (!clienteValue) {
        e.preventDefault();
        alert('Por favor, selecciona un cliente.');
        clienteSearch.focus();
        clienteSearch.classList.add('is-invalid');
        return;
    }

    const productos = document.querySelectorAll('.fila-producto');
    let isValid = true;
    productos.forEach(row => {
        const select = row.querySelector('.select-producto');
        if (!select.value) {
            isValid = false;
        }
    });

    if (!isValid) {
        e.preventDefault();
        alert('Por favor, selecciona un producto para cada fila.');
        return;
    }

    // Validar método de pago
    const metodoSeleccionado = document.querySelector('.metodo-pago:checked');
    if (metodoSeleccionado && metodoSeleccionado.value === 'efectivo') {
        const monto = parseFloat(montoRecibido.value) || 0;
        const total = parseFloat(totalGeneralElement.textContent.replace('$ ', '')) || 0;
        if (monto < total) {
            e.preventDefault();
            alert('El monto recibido es menor al total de la venta.');
        }
    }
});
});