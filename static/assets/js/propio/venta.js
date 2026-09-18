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
  

    // Buscador de productos
    const buscadorProductos = document.getElementById('buscador-productos');
    const productoSuggestions = document.getElementById('producto-suggestions');
    const btnScanBarcode = document.getElementById('btn-scan-barcode');

    // ===================== TASA DE CAMBIO (BCV) =====================
    const tasaBcv = document.getElementById('tasa-dolar-data');
    let tasaCambio = tasaBcv;

    function obtenerTasaBCV() {
        try {
            const tasaBcv = document.getElementById('tasa-dolar-data');
            console.log('Elemento de tasa BCV:', tasaBcv);
            if (tasaBcv) {
                tasaCambio = parseFloat(tasaBcv.textContent) || 36.50;
                console.log('Tasa de cambio obtenida del BCV:', tasaCambio);
            } else {
                tasaCambio = 36.50;
            }
        } catch (error) {
            console.error('Error al parsear la tasa BCV:', error);
            tasaCambio = 36.50; // Fallback
        } finally {
            // actualizarTasas();
            // Recalcular filas una vez que tenemos la tasa garantizada
            document.querySelectorAll('.fila-producto').forEach(row => {
                calcularSubtotalYTotal(row);
            });
        }
    }

    // function actualizarTasas() {
    //     const elTasaUsd = document.getElementById('tasa-usd-header');
    //     const elTasaBs = document.getElementById('tasa-bs-header');
    //     const elTasaBcv = document.getElementById('tasaBcv');

    //     if (elTasaUsd) elTasaUsd.textContent = '1.00';
    //     if (elTasaBs) elTasaBs.textContent = tasaCambio.toFixed(2);
    //     if (elTasaBcv) elTasaBcv.textContent = `1 USD = ${tasaCambio.toFixed(2)} Bs`;
    // }

    // ===================== CLIENTE - BÚSQUEDA =====================
    const clientesData = clienteSelect ? Array.from(clienteSelect.options).map(opt => ({
        id: opt.value,
        nombre: opt.getAttribute('data-nombre') || opt.textContent,
        documento: opt.getAttribute('data-documento') || ''
    })).filter(c => c.id) : [];

    if (clienteSearch) {
        clienteSearch.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();
            if (query.length < 1) {
                if (clienteSuggestions) clienteSuggestions.style.display = 'none';
                return;
            }

            const filtered = clientesData.filter(c => 
                c.nombre.toLowerCase().includes(query) || 
                c.documento.includes(query)
            );

            if (filtered.length === 0) {
                if (clienteSuggestions) {
                    clienteSuggestions.innerHTML = `
                        <div class="list-group-item text-muted text-center">
                            <i class="fas fa-user-slash me-1"></i> No se encontraron clientes
                        </div>
                    `;
                    clienteSuggestions.style.display = 'block';
                }
                return;
            }

            if (clienteSuggestions) {
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
                            if (clienteSelect) clienteSelect.value = id;
                            clienteSearch.value = cliente.nombre;
                            if (clienteNombreSeleccionado) clienteNombreSeleccionado.textContent = cliente.nombre;
                            if (clienteSeleccionado) clienteSeleccionado.classList.remove('d-none');
                            clienteSuggestions.style.display = 'none';
                        }
                    });
                });
            }
        });

        document.addEventListener('click', function(e) {
            if (clienteSuggestions && !clienteSearch.contains(e.target) && !clienteSuggestions.contains(e.target)) {
                clienteSuggestions.style.display = 'none';
            }
        });
    }

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

    if (buscadorProductos) {
        buscadorProductos.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();
            if (query.length < 1) {
                if (productoSuggestions) productoSuggestions.style.display = 'none';
                return;
            }

            const filtered = productosData.filter(p => 
                p.nombre.toLowerCase().includes(query) || 
                p.codigo.includes(query)
            ).slice(0, 10);

            if (filtered.length === 0) {
                if (productoSuggestions) {
                    productoSuggestions.innerHTML = `
                        <div class="list-group-item text-muted text-center">
                            <i class="fas fa-box-open me-1"></i> No se encontraron productos
                        </div>
                    `;
                    productoSuggestions.style.display = 'block';
                }
                return;
            }

            if (productoSuggestions) {
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
                        let targetRow = null;
                        document.querySelectorAll('.fila-producto').forEach(row => {
                            const select = row.querySelector('.select-producto');
                            if (select && !select.value) {
                                targetRow = row;
                            }
                        });
                        
                        if (!targetRow && addButton) {
                            addButton.click();
                            targetRow = document.querySelector('.fila-producto:last-child');
                        }
                        
                        if (targetRow) {
                            const select = targetRow.querySelector('.select-producto');
                            if (select) {
                                select.value = id;
                                const event = new Event('change');
                                select.dispatchEvent(event);
                            }
                        }
                        
                        buscadorProductos.value = '';
                        productoSuggestions.style.display = 'none';
                    });
                });
            }
        });

        document.addEventListener('click', function(e) {
            if (productoSuggestions && !buscadorProductos.contains(e.target) && !productoSuggestions.contains(e.target)) {
                productoSuggestions.style.display = 'none';
            }
        });
    }

    if (btnScanBarcode) {
        btnScanBarcode.addEventListener('click', function() {
            alert('📷 Escaneo de código de barras activado.\nPor favor, acerca el código a la cámara.');
            const codigoSimulado = prompt('Ingresa el código de barras (simulación):');
            if (codigoSimulado && buscadorProductos) {
                buscadorProductos.value = codigoSimulado;
                const event = new Event('input');
                buscadorProductos.dispatchEvent(event);
            }
        });
    }

    // ===================== CÁLCULOS =====================
    function calcularSubtotalYTotal(row) {
        const select = row.querySelector('.select-producto');
        const inputCantidad = row.querySelector('.input-cantidad');
        const precioVisual = row.querySelector('.precio-visual');
        const precioVisualBolivares = row.querySelector('.precio-visual-bs');
        const subtotalVisual = row.querySelector('.subtotal-visual');
        const subtotalVisualBolivares = row.querySelector('.subtotal-visual-bs');
        const stockIndicator = row.querySelector('.stock-indicator');

        if (!select) return;

        const selectedOption = select.options[select.selectedIndex];
        const precio = selectedOption ? parseFloat(selectedOption.getAttribute('data-precio')) || 0 : 0;
        const stock = selectedOption ? parseInt(selectedOption.getAttribute('data-stock')) || 0 : 0;
        let cantidad = inputCantidad ? (parseInt(inputCantidad.value) || 0) : 0;

        if (stockIndicator && inputCantidad) {
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
        }

        if (precioVisual) precioVisual.value = `$ ${precio.toFixed(2)}`;
        if (precioVisualBolivares) precioVisualBolivares.value = `Bs ${(precio * tasaCambio).toFixed(2)}`;
        
        const subtotal = precio * cantidad;
        if (subtotalVisual) subtotalVisual.value = `$ ${subtotal.toFixed(2)}`;
        if (subtotalVisualBolivares) subtotalVisualBolivares.value = `Bs ${(subtotal * tasaCambio).toFixed(2)}`;
        calcularTotalesGenerales();
    }

    function calcularTotalesGenerales() {
        let total = 0;
        let totalItems = 0;
        let totalProductos = 0;

        document.querySelectorAll('.fila-producto').forEach(row => {
            const select = row.querySelector('.select-producto');
            const inputCantidad = row.querySelector('.input-cantidad');
            if (select && select.value) {
                const selectedOption = select.options[select.selectedIndex];
                const precio = parseFloat(selectedOption.getAttribute('data-precio')) || 0;
                const cantidad = inputCantidad ? (parseInt(inputCantidad.value) || 0) : 0;

                totalProductos++;
                totalItems += cantidad;
                total += precio * cantidad;
            }
        });

        const descuento = descuentoInput ? (parseFloat(descuentoInput.value) || 0) : 0;
        const subtotal = total;
        const iva = subtotal * 0.16;
        const totalConIva = subtotal + iva;
        const totalConDescuento = totalConIva - descuento;

        if (desgloseSubtotal) desgloseSubtotal.textContent = `$ ${subtotal.toFixed(2)}`;
        if (desgloseIva) desgloseIva.textContent = `$ ${iva.toFixed(2)}`;
        if (desgloseTotalIva) desgloseTotalIva.textContent = `$ ${totalConIva.toFixed(2)}`;
        if (desgloseTotalDescuento) desgloseTotalDescuento.textContent = `$ ${totalConDescuento.toFixed(2)}`;

        const totalFinal = Math.max(totalConDescuento, 0);
        if (totalGeneralElement) totalGeneralElement.textContent = `$ ${totalFinal.toFixed(2)}`;
        
        const totalBsValue = totalFinal * tasaCambio;
        if (totalGeneralBs) totalGeneralBs.textContent = `Bs ${totalBsValue.toFixed(2)}`;
        if (totalBs) totalBs.textContent = `Bs ${totalBsValue.toFixed(2)}`;

        const elTotalDolares = document.getElementById('total-dolares');
        if (elTotalDolares) elTotalDolares.textContent = `$ ${totalFinal.toFixed(2)}`;

        const elResumenProductos = document.getElementById('resumen-productos');
        if (elResumenProductos) elResumenProductos.textContent = totalProductos;

        const elResumenItems = document.getElementById('resumen-items');
        if (elResumenItems) elResumenItems.textContent = totalItems;

        const elResumenSubtotal = document.getElementById('resumen-subtotal');
        if (elResumenSubtotal) elResumenSubtotal.textContent = `$ ${subtotal.toFixed(2)}`;

        const elResumenSubtotalBs = document.getElementById('resumen-subtotal-bs');
        if (elResumenSubtotalBs) elResumenSubtotalBs.textContent = `Bs ${(subtotal * tasaCambio).toFixed(2)}`;

        const elProductCount = document.getElementById('product-count');
        if (elProductCount) elProductCount.textContent = `${totalProductos} productos`;

        calcularCambio(totalFinal);
    }

    function calcularCambio(total) {
        if (!montoRecibido || !montoCambio) return;
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
                if (efectivoFields) efectivoFields.classList.remove('d-none');
                if (creditoFields) creditoFields.classList.add('d-none');
            } else if (this.value === 'credito') {
                if (efectivoFields) efectivoFields.classList.add('d-none');
                if (creditoFields) creditoFields.classList.remove('d-none');
            } else {
                if (efectivoFields) efectivoFields.classList.add('d-none');
                if (creditoFields) creditoFields.classList.add('d-none');
            }
        });
    });

    if (montoRecibido) {
        montoRecibido.addEventListener('input', function() {
            calcularTotalesGenerales();
        });
    }

    if (descuentoInput) {
        descuentoInput.addEventListener('input', function() {
            calcularTotalesGenerales();
        });
    }

    // ===================== EVENTOS DE TABLA =====================
    if (tableBody) {
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
    }

    // ===================== AGREGAR PRODUCTO =====================
    if (addButton) {
        addButton.addEventListener('click', function() {
            const firstRow = document.querySelector('.fila-producto');
            if (!firstRow) return;

            const newRow = firstRow.cloneNode(true);
            
            const select = newRow.querySelector('.select-producto');
            const cantidadInput = newRow.querySelector('.input-cantidad');
            const precioVisual = newRow.querySelector('.precio-visual');
            const subtotalVisual = newRow.querySelector('.subtotal-visual');
            const stockIndicator = newRow.querySelector('.stock-indicator');

            if (select) select.selectedIndex = 0;
            if (cantidadInput) cantidadInput.value = 1;
            if (precioVisual) precioVisual.value = '$ 0.00';
            if (subtotalVisual) subtotalVisual.value = '$ 0.00';
            if (stockIndicator) {
                stockIndicator.className = 'badge stock-indicator bg-success rounded-pill';
                stockIndicator.textContent = 'Disponible';
            }

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
    }

    // ===================== VALIDACIÓN ANTES DE ENVIAR =====================
    const formVenta = document.getElementById('form-venta');
    if (formVenta) {
        formVenta.addEventListener('submit', function(e) {
            if (clienteSelect) {
                const clienteValue = clienteSelect.value;
                if (!clienteValue) {
                    e.preventDefault();
                    alert('Por favor, selecciona un cliente.');
                    if (clienteSearch) {
                        clienteSearch.focus();
                        clienteSearch.classList.add('is-invalid');
                    }
                    return;
                }
            }

            const productos = document.querySelectorAll('.fila-producto');
            let isValid = true;
            productos.forEach(row => {
                const select = row.querySelector('.select-producto');
                if (select && !select.value) {
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Por favor, selecciona un producto para cada fila.');
                return;
            }

            const metodoSeleccionado = document.querySelector('.metodo-pago:checked');
            if (metodoSeleccionado && metodoSeleccionado.value === 'efectivo' && montoRecibido && totalGeneralElement) {
                const monto = parseFloat(montoRecibido.value) || 0;
                const total = parseFloat(totalGeneralElement.textContent.replace('$ ', '')) || 0;
                if (monto < total) {
                    e.preventDefault();
                    alert('El monto recibido es menor al total de la venta.');
                }
            }
        });
    }

    // ===================== INICIALIZACIÓN =====================
    obtenerTasaBCV();
});