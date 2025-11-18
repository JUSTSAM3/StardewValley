
// CAMBIO DE SECCIONES
document.querySelectorAll(".menu-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        document.querySelectorAll(".menu-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        const section = btn.dataset.section;

        document.querySelectorAll(".admin-section").forEach(sec => sec.classList.remove("visible"));
        document.getElementById("section-" + section).classList.add("visible");

        // cargar datos de la sección
        loadSection(section);
    });
});

// On initial load, trigger load for the active section (so tables populate without needing a manual click)
setTimeout(() => {
    const active = document.querySelector('.menu-btn.active');
    if (active && active.dataset && active.dataset.section) {
        loadSection(active.dataset.section);
    }
}, 20);

// Logout button handler
const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
        openLogoutConfirm();
    });
}
function openLogoutConfirm() {
    openModal('modal-logout-confirm');
}

function confirmLogout() {
    window.location.href = '/logout';
}

function cancelLogout() {
    closeModal('modal-logout-confirm');
}

// FUNCIONES POR SECCIÓN

async function loadSection(section) {
    try {
        if (section === "resumen") return loadResumen();
        if (section === "animales") return loadAnimales();
        if (section === "cultivos") return loadCultivos();
        if (section === "recursos") return loadRecursos();
        if (section === "maquinaria") return loadMaquinaria();
        if (section === "empleados") return loadEmpleados();
        if (section === "productos") return loadProductos();
        if (section === "clientes") return loadClientes();
        if (section === "ventas") return loadVentas();
    } catch (e) {
        console.error(e);
        showError('main', 'Error cargando sección.');
    }
}

// UTILIDADES
function showError(section, msg) {
    const box = document.querySelector(`#section-${section} .section-content`);
    if (box) box.innerHTML = `<p style="color:red">${msg}</p>`;
}

// Small loading helper to display while fetching data
function showLoading(section) {
    const box = document.querySelector(`#section-${section} .section-content`);
    if (box) box.innerHTML = `<div class="loading" style="padding:12px; color:#666">Cargando...</div>`;
}

// Modal inline error 
function showModalError(prefix, msg) {
    const el = document.getElementById(prefix + '-error');
    if (el) el.textContent = msg || '';
    else alert(msg);
}

function clearModalError(prefix) {
    const el = document.getElementById(prefix + '-error');
    if (el) el.textContent = '';
}

// Modal inline success 
function showModalSuccess(prefix, msg) {
    const elId = prefix + '-success';
    let el = document.getElementById(elId);
    if (!el) {
        // create a small success area under existing error area
        const container = document.getElementById(prefix + '-error')?.parentNode;
        if (container) {
            el = document.createElement('div');
            el.id = elId;
            el.className = 'error-message-inline';
            el.style.color = '#065f46';
            container.insertBefore(el, container.firstChild);
        }
    }
    if (el) el.textContent = msg || '';
}

function clearModalSuccess(prefix) {
    const el = document.getElementById(prefix + '-success');
    if (el) el.textContent = '';
}

// Generic open/close modal helpers with focus management
function openModal(modalId, firstSelector) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    // store previously focused element to restore later
    modal.dataset.prevFocus = document.activeElement ? document.activeElement.id || document.activeElement.tagName : '';
    modal.style.display = 'flex';
    clearModalError(modalId.replace('modal-',''));
    clearModalSuccess(modalId.replace('modal-',''));
    // focus first field
    setTimeout(() => {
        const first = modal.querySelector(firstSelector) || modal.querySelector('input, select, textarea, button');
        if (first) first.focus();
    }, 50);
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    modal.style.display = 'none';
    const prev = modal.dataset.prevFocus;
    if (prev) {
        const el = document.getElementById(prev);
        if (el) el.focus();
    }
}

function fillTable(section, headers, rows) {
    const box = document.querySelector(`#section-${section} .section-content`);
    if (!box) return;
    // Build table HTML (actions column will contain buttons with data-attrs)
    let html = "<table class='data-table'><thead><tr>";
    headers.forEach(h => html += `<th>${h}</th>`);
    html += "<th>Acciones</th></tr></thead><tbody>";

    if (!rows || rows.length === 0) {
        html += `<tr><td colspan="${headers.length + 1}">Sin datos</td></tr>`;
    } else {
        rows.forEach((r, idx) => {
            html += "<tr>";
            headers.forEach(h => {
                const val = r[h] == null ? '' : r[h];
                html += `<td>${val}</td>`;
            });

            // Use data attributes to avoid inline JS escaping issues
            const idVal = r[headers[0]];
            const dataJson = encodeURIComponent(JSON.stringify(r));
            // Add Assign button for sections that support assignments
            let actionsHtml = `<button class="btn-edit" data-section="${section}" data-json="${dataJson}">Editar</button>`;
            if (section === 'animales' || section === 'maquinaria' || section === 'cultivos') {
                actionsHtml += ` <button class="btn-assign" data-section="${section}" data-id="${idVal}">Asignar</button>`;
            }
            actionsHtml += ` <button class="btn-delete" data-section="${section}" data-id="${idVal}">Eliminar</button>`;
            html += `\n<td>\n  ${actionsHtml}\n</td>\n`;

            html += "</tr>";
        });
    }

    html += "</tbody></table>";
    box.innerHTML = html;

    // Attach handlers for edit and delete buttons
    box.querySelectorAll('.btn-edit').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const section = btn.dataset.section;
            const json = btn.dataset.json ? JSON.parse(decodeURIComponent(btn.dataset.json)) : null;
            try {
                const fn = window[`edit_${section}`];
                if (typeof fn === 'function') fn(json);
            } catch (err) {
                console.error('edit handler error', err);
            }
        });
    });

    box.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const section = btn.dataset.section;
            const id = btn.dataset.id;
            try {
                const fn = window[`delete_${section}`];
                if (typeof fn === 'function') {
                    // call delete handler; if it expects id param, pass it
                    fn(id);
                }
            } catch (err) {
                console.error('delete handler error', err);
            }
        });
    });

    // Attach assign handlers
    box.querySelectorAll('.btn-assign').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const section = btn.dataset.section;
            const id = btn.dataset.id;
            openAssignModal(section, id);
        });
    });
}


// RESUMEN
async function loadResumen() {
    try {
        showLoading('resumen');
        // --- Consultas reales por separado ---
        const animales = await fetch("/api/animales").then(r => r.json());
        const cultivos = await fetch("/api/cultivos").then(r => r.json());
        const productos = await fetch("/api/productos").then(r => r.json());
        const ventas = await fetch("/api/ventas").then(r => r.json());

        // Totales
        const total_animales = animales.length;
        const total_cultivos = cultivos.length;
        const total_productos = productos.length;

        let total_ventas_mes = 0;

        // Sumar ventas del mes actual
        const hoy = new Date();
        const mes = hoy.getMonth() + 1;
        const año = hoy.getFullYear();

        ventas.forEach(v => {
            const f = new Date(v.fecha);
            if (f.getMonth() + 1 === mes && f.getFullYear() === año) {
                total_ventas_mes += parseFloat(v.total);
            }
        });

        // Pintar tarjetas
        const box = document.querySelector("#section-resumen .section-content");
        box.innerHTML = `
            <div class="cards-grid">

                <article class="mini-card">
                    <h3>Total animales</h3>
                    <p style="font-size:1.4rem; font-weight:bold;">${total_animales}</p>
                </article>

                <article class="mini-card">
                    <h3>Total cultivos</h3>
                    <p style="font-size:1.4rem; font-weight:bold;">${total_cultivos}</p>
                </article>

                <article class="mini-card">
                    <h3>Total productos</h3>
                    <p style="font-size:1.4rem; font-weight:bold;">${total_productos}</p>
                </article>

                <article class="mini-card">
                    <h3>Ventas este mes</h3>
                    <p style="font-size:1.4rem; font-weight:bold;">$${total_ventas_mes}</p>
                </article>

            </div>
        `;
    } catch (e) {
        console.error(e);
        showError("resumen", "Error cargando resumen.");
    }
}


// ANIMALES
async function loadAnimales() {
    // Load animals plus empleado assignments to show responsables
    showLoading('animales');
    const [res, relRes, empRes] = await Promise.all([
        fetch('/api/animales'),
        fetch('/api/empleado_animal'),
        fetch('/api/empleados')
    ]);
    const data = await res.json();
    const rel = await relRes.json();
    const emps = await empRes.json();
    const empMap = {};
    (emps || []).forEach(e => { empMap[e.identificacion] = e.nombre; });
    (data || []).forEach(a => {
        const assigned = (rel || []).filter(r => r.id_animal == a.id).map(r => empMap[r.identificacion] || r.identificacion);
        a.responsables = assigned.join(', ');
    });
    fillTable("animales", ["id", "nombre", "especie", "raza", "sexo", "estado", "responsables"], data);
}

// CULTIVOS
async function loadCultivos() {
    // Load cultivos plus empleado assignments
    showLoading('cultivos');
    const [res, relRes, empRes] = await Promise.all([
        fetch('/api/cultivos'),
        fetch('/api/empleado_cultivo'),
        fetch('/api/empleados')
    ]);
    const data = await res.json();
    const rel = await relRes.json();
    const emps = await empRes.json();
    const empMap = {};
    (emps || []).forEach(e => { empMap[e.identificacion] = e.nombre; });
    (data || []).forEach(c => {
        const assigned = (rel || []).filter(r => r.id_cultivo == c.id).map(r => empMap[r.identificacion] || r.identificacion);
        c.responsables = assigned.join(', ');
    });
    fillTable("cultivos", ["id", "nombre", "tipo", "epoca", "estado", "fecha_siembra", "responsables"], data);
}

// RECURSOS
async function loadRecursos() {
    showLoading('recursos');
    const res = await fetch("/api/recursos");
    const data = await res.json();
    fillTable("recursos", ["id", "nombre", "tipo_recurso", "stock"], data);
}

// MAQUINARIA
async function loadMaquinaria() {
    // Load maquinaria plus empleado assignments
    showLoading('maquinaria');
    const [res, relRes, empRes] = await Promise.all([
        fetch('/api/maquinaria'),
        fetch('/api/empleado_maquinaria'),
        fetch('/api/empleados')
    ]);
    const data = await res.json();
    const rel = await relRes.json();
    const emps = await empRes.json();
    const empMap = {};
    (emps || []).forEach(e => { empMap[e.identificacion] = e.nombre; });
    (data || []).forEach(m => {
        const assigned = (rel || []).filter(r => r.id_maquinaria == m.id).map(r => empMap[r.identificacion] || r.identificacion);
        m.responsables = assigned.join(', ');
    });
    fillTable("maquinaria", ["id", "nombre", "tipo", "modelo", "estado", "responsables"], data);
}

// EMPLEADOS
async function loadEmpleados() {
    showLoading('empleados');
    const res = await fetch("/api/empleados");
    const data = await res.json();
    fillTable("empleados", ["identificacion", "nombre", "cargo", "fecha_ingreso", "sueldo"], data);
}

// PRODUCTOS
async function loadProductos() {
    showLoading('productos');
    const res = await fetch("/api/productos");
    const data = await res.json();
    fillTable("productos", ["identificacion", "nombre", "tipo", "precio"], data);
}

// PRODUCTOS CRUD (modal)
function openProductoForm(existing) {
    const modalId = 'modal-producto';
    openModal(modalId, '#producto-identificacion');
    document.getElementById('producto-modal-title').textContent = existing ? 'Editar Producto' : 'Nuevo Producto';
    document.getElementById('producto-identificacion').value = existing ? existing.identificacion : '';
    document.getElementById('producto-identificacion').disabled = existing ? true : false;
    document.getElementById('producto-nombre').value = existing ? existing.nombre : '';
    document.getElementById('producto-tipo').value = existing ? existing.tipo : '';
    document.getElementById('producto-precio').value = existing ? existing.precio : '';
    document.getElementById(modalId).dataset.editId = existing ? existing.identificacion : '';
}

function closeProductoForm() {
    document.getElementById('modal-producto').dataset.editId = '';
    document.getElementById('producto-identificacion').disabled = false;
    closeModal('modal-producto');
}

async function saveProducto() {
    const editId = document.getElementById('modal-producto').dataset.editId;
    const payload = {
        identificacion: document.getElementById('producto-identificacion').value,
        nombre: document.getElementById('producto-nombre').value,
        tipo: document.getElementById('producto-tipo').value,
        precio: document.getElementById('producto-precio').value
    };
    try {
        if (editId) {
            await fetch(`/api/productos/${editId}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        } else {
            await fetch('/api/productos', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        }
        showModalSuccess('producto','Guardado correctamente');
        setTimeout(() => { closeProductoForm(); loadProductos(); }, 700);
    } catch (e) {
        showModalError('producto','Error guardando producto');
    }
}

async function edit_productos(data) { openProductoForm(data); }

async function delete_productos(id) {
    if (!confirm('¿Eliminar producto?')) return;
    try {
        const res = await fetch(`/api/productos/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (!res.ok || !data.ok) {
            showModalError('producto', data.error || 'Error eliminando producto');
            return;
        }
        loadProductos();
    } catch (e) {
        console.error(e);
        showModalError('producto','Error eliminando producto');
    }
}

// CLIENTES
async function loadClientes() {
    showLoading('clientes');
    const res = await fetch("/api/clientes");
    const data = await res.json();
    fillTable("clientes", ["documento", "nombre", "direccion", "telefono", "email"], data);
}

// VENTAS
async function loadVentas() {
    showLoading('ventas');
    const res = await fetch("/api/ventas");
    const data = await res.json();
    fillTable("ventas", ["id", "cliente_nombre", "fecha", "total"], data);
}

// VENTAS (simple modal create)
function openVentaForm() {
    const modalId = 'modal-venta';
    openModal(modalId, '#venta-cliente');
    // load products into selector cache and create an empty row
    if (!window.productosCache || window.productosCache.length === 0) {
        fetch('/api/productos').then(r => r.json()).then(list => { window.productosCache = list; addVentaRow(); }).catch(e => { console.error(e); addVentaRow(); });
    } else {
        // ensure at least one row
        const tbody = document.querySelector('#venta-table tbody');
        if (!tbody || tbody.children.length === 0) addVentaRow();
    }
    // populate clients datalist
    fetch('/api/clientes').then(r => r.json()).then(list => {
        window.clientesCache = list || [];
        const dl = document.getElementById('clientes-list');
        if (dl) {
            dl.innerHTML = '';
            (list || []).forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.documento;
                opt.textContent = c.nombre;
                dl.appendChild(opt);
            });
        }
    }).catch(e => console.error('Error cargando clientes', e));
}

function openClienteFromVenta() {
    const documento = document.getElementById('venta-cliente').value;
    openClienteForm();
    // Poner el modal de cliente encima del modal de venta
    const clienteModal = document.getElementById('modal-cliente');
    if (clienteModal) {
        clienteModal.classList.add('modal-top');
    }
    if (documento && documento.trim() !== '') {
        document.getElementById('cliente-documento').value = documento;
    }
}

function closeVentaForm() {
    // clear rows
    const tbody = document.querySelector('#venta-table tbody');
    if (tbody) tbody.innerHTML = '';
    document.getElementById('venta-subtotal').textContent = '0.00';
    document.getElementById('venta-total').textContent = '0.00';
    closeModal('modal-venta');
}

async function saveVenta() {
    const documento = document.getElementById('venta-cliente').value;
    // validate cliente
    if (!documento || documento.trim() === '') { showModalError('venta','Documento de cliente requerido'); return; }

    // check cliente exists
    try {
        const resp = await fetch(`/api/clientes/${encodeURIComponent(documento)}`);
        if (resp.status === 404) {
            // prompt to create
            const create = confirm('Cliente no existe. ¿Deseas crearlo ahora?');
            if (create) {
                openClienteForm();
                document.getElementById('cliente-documento').value = documento;
            }
            return;
        }
        if (!resp.ok) {
            showModalError('venta','Error verificando cliente');
            return;
        }
    } catch (e) {
        console.error(e);
        showModalError('venta','Error verificando cliente');
        return;
    }

    // gather rows
    const rows = Array.from(document.querySelectorAll('#venta-table tbody tr'));
    if (rows.length === 0) { showModalError('venta','Agrega al menos un producto'); return; }

    const items = [];
    for (const r of rows) {
        const sel = r.querySelector('select');
        const prodId = sel ? sel.value : '';
        const qty = parseFloat(r.querySelector('.venta-cantidad').value || '0');
        const price = parseFloat(r.querySelector('.venta-precio').value || '0');
        if (!prodId) { showModalError('venta','Selecciona un producto en todas las filas'); return; }
        if (!(qty > 0)) { showModalError('venta','Cantidad debe ser mayor que 0'); return; }
        items.push({ identificacion_producto: prodId, cantidad: qty, precio_unit: price });
    }

    try {
        await fetch('/api/ventas', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ documento_cliente: documento, items }) });
        closeVentaForm();
        loadVentas();
    } catch (e) {
        console.error(e);
        showModalError('venta','Error creando venta');
    }
}

// Product picker helpers for venta
function addVentaRow(productId, cantidad) {
    const tbody = document.querySelector('#venta-table tbody');
    if (!tbody) return;
    const tr = document.createElement('tr');

    // product select
    const tdProd = document.createElement('td');
    const sel = document.createElement('select');
    sel.innerHTML = `<option value="">-- seleccionar --</option>`;
    const prods = window.productosCache || [];
    prods.forEach(p => sel.innerHTML += `<option value="${p.identificacion}" data-precio="${p.precio}">${p.nombre} (${p.identificacion})</option>`);
    if (productId) sel.value = productId;
    sel.addEventListener('change', () => {
        const precio = parseFloat(sel.selectedOptions[0].dataset.precio || '0');
        tr.querySelector('.venta-precio').value = precio;
        updateRowSubtotal(tr);
    });
    tdProd.appendChild(sel);

    // cantidad
    const tdQty = document.createElement('td');
    const inpQty = document.createElement('input'); inpQty.type = 'number'; inpQty.min = '0'; inpQty.value = cantidad || 1; inpQty.className = 'venta-cantidad';
    inpQty.addEventListener('input', () => updateRowSubtotal(tr));
    tdQty.appendChild(inpQty);

    // precio
    const tdPrice = document.createElement('td');
    const inpPrice = document.createElement('input'); inpPrice.type = 'number'; inpPrice.step = '0.01'; inpPrice.className = 'venta-precio'; inpPrice.readOnly = true; inpPrice.value = '0.00';
    tdPrice.appendChild(inpPrice);

    // subtotal
    const tdSub = document.createElement('td'); tdSub.className = 'venta-subcell'; tdSub.textContent = '0.00';

    // remove
    const tdRem = document.createElement('td');
    const btnRem = document.createElement('button'); btnRem.type = 'button'; btnRem.className = 'btn'; btnRem.textContent = 'Eliminar';
    btnRem.addEventListener('click', () => { tr.remove(); computeVentaTotals(); });
    tdRem.appendChild(btnRem);

    tr.appendChild(tdProd); tr.appendChild(tdQty); tr.appendChild(tdPrice); tr.appendChild(tdSub); tr.appendChild(tdRem);
    tbody.appendChild(tr);

    // if productId provided, trigger change to set price
    if (productId) {
        sel.dispatchEvent(new Event('change'));
    }
    computeVentaTotals();
}

function updateRowSubtotal(tr) {
    const qty = parseFloat(tr.querySelector('.venta-cantidad').value || '0');
    const price = parseFloat(tr.querySelector('.venta-precio').value || '0');
    const sub = (qty * price) || 0;
    tr.querySelector('.venta-subcell').textContent = sub.toFixed(2);
    computeVentaTotals();
}

function computeVentaTotals() {
    let total = 0;
    document.querySelectorAll('#venta-table tbody tr').forEach(tr => {
        const s = parseFloat(tr.querySelector('.venta-subcell').textContent || '0') || 0;
        total += s;
    });
    document.getElementById('venta-subtotal').textContent = total.toFixed(2);
    document.getElementById('venta-total').textContent = total.toFixed(2);
}

// attach add-row button when script loads
document.addEventListener('click', (e) => {
    if (e.target && e.target.id === 'venta-add-row') {
        // if products not loaded, fetch then add
        if (!window.productosCache || window.productosCache.length === 0) {
            fetch('/api/productos').then(r => r.json()).then(list => { window.productosCache = list; addVentaRow(); }).catch(e => { console.error(e); addVentaRow(); });
        } else addVentaRow();
    }
});

async function edit_ventas(data) { showModalError('venta','Editar ventas no implementado'); }

async function delete_ventas(id) {
    if (!confirm('¿Eliminar venta?')) return;
    try {
        const res = await fetch(`/api/ventas/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (!res.ok || !data.ok) {
            showModalError('venta', data.error || 'Error eliminando venta');
            return;
        }
        loadVentas();
    } catch (e) {
        console.error(e);
        showModalError('venta','Error eliminando venta');
    }
}

async function delete_animales(id) {
    if (!confirm("¿Eliminar animal?")) return;

    try {
        const res = await fetch(`/api/animales/${id}`, { method: "DELETE" });
        const data = await res.json();
        if (!res.ok || !data.ok) {
            showModalError('animal', data.error || 'Error eliminando animal');
            return;
        }
        loadAnimales();
    } catch (e) {
        console.error(e);
        showModalError('animal', 'Error eliminando animal');
    }
}

async function delete_cultivos(id) {
    if (!confirm("¿Eliminar cultivo?")) return;

    try {
        const res = await fetch(`/api/cultivos/${id}`, { method: "DELETE" });
        const data = await res.json();
        if (!res.ok || !data.ok) {
            showModalError('cultivo', data.error || 'Error eliminando cultivo');
            return;
        }
        loadCultivos();
    } catch (e) {
        console.error(e);
        showModalError('cultivo', 'Error eliminando cultivo');
    }
}

async function edit_cultivos(data) {
    openCultivoForm(data);
}

// ---------- CULTIVO MODAL HANDLERS ----------
function openCultivoForm(existing) {
    const modalId = 'modal-cultivo';
    openModal(modalId, '#cultivo-nombre');
    document.getElementById('cultivo-modal-title').textContent = existing ? 'Editar Cultivo' : 'Nuevo Cultivo';
    document.getElementById('cultivo-nombre').value = existing ? existing.nombre : '';
    document.getElementById('cultivo-tipo').value = existing ? existing.tipo : '';
    document.getElementById('cultivo-epoca').value = existing ? existing.epoca : '';
    document.getElementById('cultivo-estado').value = existing ? existing.estado : 'SEMILLA';
    document.getElementById('cultivo-fecha').value = existing ? existing.fecha_siembra : '';
    document.getElementById(modalId).dataset.editId = existing ? existing.id : '';
}

function closeCultivoForm() {
    document.getElementById('modal-cultivo').dataset.editId = '';
    closeModal('modal-cultivo');
}

async function saveCultivo() {
    const editId = document.getElementById('modal-cultivo').dataset.editId;
    const payload = {
        nombre: document.getElementById('cultivo-nombre').value,
        tipo: document.getElementById('cultivo-tipo').value,
        epoca: document.getElementById('cultivo-epoca').value,
        estado: document.getElementById('cultivo-estado').value,
        fecha_siembra: document.getElementById('cultivo-fecha').value
    };
    try {
        if (editId) {
            await fetch(`/api/cultivos/${editId}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        } else {
            await fetch('/api/cultivos', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        }
        showModalSuccess('cultivo','Guardado correctamente');
        setTimeout(() => { closeCultivoForm(); loadCultivos(); }, 700);
    } catch (e) {
        showModalError('cultivo','Error guardando cultivo');
    }
}
// ---------- ANIMAL MODAL HANDLERS ----------
function openAnimalForm(existing) {
    const modalId = 'modal-animal';
    openModal(modalId, '#animal-nombre');
    document.getElementById('animal-modal-title').textContent = existing ? 'Editar Animal' : 'Nuevo Animal';
    document.getElementById('animal-nombre').value = existing ? existing.nombre : '';
    document.getElementById('animal-especie').value = existing ? existing.especie : '';
    document.getElementById('animal-raza').value = existing ? existing.raza : '';
    document.getElementById('animal-sexo').value = existing ? existing.sexo : '';
    document.getElementById('animal-estado').value = existing ? existing.estado : '';
    // store id on modal element for editing
    document.getElementById(modalId).dataset.editId = existing ? existing.id : '';
}

function closeAnimalForm() {
    document.getElementById('modal-animal').dataset.editId = '';
    closeModal('modal-animal');
}

async function saveAnimal() {
    const id = document.getElementById('modal-animal').dataset.editId;
    const payload = {
        nombre: document.getElementById('animal-nombre').value,
        especie: document.getElementById('animal-especie').value,
        raza: document.getElementById('animal-raza').value,
        sexo: document.getElementById('animal-sexo').value,
        estado: document.getElementById('animal-estado').value
    };
    try {
        if (id) {
            await fetch(`/api/animales/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        } else {
            await fetch('/api/animales', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        }
        showModalSuccess('animal','Guardado correctamente');
        setTimeout(() => { closeAnimalForm(); loadAnimales(); }, 700);
    } catch (e) {
        showModalError('animal','Error guardando animal');
        console.error(e);
    }
}

// Modify edit_animales to open modal
async function edit_animales(data) {
    openAnimalForm(data);
}

// Modal-based empleados handlers
function openEmpleadoForm(existing) {
    const modalId = 'modal-empleado';
    openModal(modalId, '#empleado-identificacion');
    document.getElementById('empleado-modal-title').textContent = existing ? 'Editar Empleado' : 'Nuevo Empleado';
    document.getElementById('empleado-identificacion').value = existing ? existing.identificacion : '';
    document.getElementById('empleado-identificacion').disabled = existing ? true : false;
    document.getElementById('empleado-nombre').value = existing ? existing.nombre : '';
    document.getElementById('empleado-cargo').value = existing ? existing.cargo : '';
    document.getElementById('empleado-fecha').value = existing ? existing.fecha_ingreso : '';
    document.getElementById('empleado-sueldo').value = existing ? existing.sueldo : '';
    document.getElementById(modalId).dataset.editId = existing ? existing.identificacion : '';
}

function closeEmpleadoForm() {
    document.getElementById('empleado-identificacion').disabled = false;
    document.getElementById('modal-empleado').dataset.editId = '';
    closeModal('modal-empleado');
}

async function saveEmpleado() {
    const editId = document.getElementById('modal-empleado').dataset.editId;
    const payload = {
        identificacion: document.getElementById('empleado-identificacion').value,
        nombre: document.getElementById('empleado-nombre').value,
        cargo: document.getElementById('empleado-cargo').value,
        fecha_ingreso: document.getElementById('empleado-fecha').value,
        sueldo: document.getElementById('empleado-sueldo').value
    };
    try {
        if (editId) {
            await fetch(`/api/empleados/${editId}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        } else {
            await fetch('/api/empleados', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        }
        showModalSuccess('empleado','Guardado correctamente');
        setTimeout(() => { closeEmpleadoForm(); loadEmpleados(); }, 700);
    } catch (e) {
        showModalError('empleado','Error guardando empleado');
    }
}

async function edit_empleados(data) { openEmpleadoForm(data); }

async function delete_empleados(id) {
    // Always use server-side cascade endpoint which removes assignments (keeps items)
    try {
        // fetch assignments just to display details in confirmation
        const [animalRes, maqRes, cultRes] = await Promise.all([
            fetch('/api/empleado_animal'),
            fetch('/api/empleado_maquinaria'),
            fetch('/api/empleado_cultivo')
        ]);
        const [animalList, maqList, cultList] = await Promise.all([animalRes.json(), maqRes.json(), cultRes.json()]);

        const assignedAnimals = (animalList || []).filter(a => a.identificacion === id);
        const assignedMaquinas = (maqList || []).filter(m => m.identificacion === id);
        const assignedCultivos = (cultList || []).filter(c => c.identificacion === id);

        const details = [];
        if (assignedAnimals.length) assignedAnimals.forEach(a => details.push(`Animal ID: ${a.id_animal}`));
        if (assignedMaquinas.length) assignedMaquinas.forEach(m => details.push(`Maquinaria ID: ${m.id_maquinaria}`));
        if (assignedCultivos.length) assignedCultivos.forEach(c => details.push(`Cultivo ID: ${c.id_cultivo}`));

        const message = `Se eliminará el empleado y se quitarán sus asignaciones. Los animales, cultivos y maquinarias permanecerán pero sin responsable. ¿Continuar?`;

        openDeleteConfirm(message, details, async () => {
            try {
                const resp = await fetch(`/api/empleados/${id}/cascade`, { method: 'DELETE' });
                const result = await resp.json();
                if (!resp.ok || !(result && result.ok)) throw new Error(result.error || 'Error en borrado en cascada');
                closeDeleteConfirm();
                showModalSuccess('empleado', `Empleado eliminado. Asignaciones removidas - animales: ${result.deleted_relations.animal}, maquinarias: ${result.deleted_relations.maquinaria}, cultivos: ${result.deleted_relations.cultivo}`);
                setTimeout(() => { loadEmpleados(); }, 800);
            } catch (err) {
                console.error(err);
                showModalError('empleado','Error eliminando empleado o sus asignaciones');
            }
        });

    } catch (e) {
        console.error(e);
        showModalError('empleado','Error verificando asignaciones del empleado');
    }
}

// Generic delete-confirm modal helpers
window._pendingDeleteCallback = null;
function openDeleteConfirm(message, details, onConfirm) {
    const modalId = 'modal-delete-confirm';
    const msgEl = document.getElementById('delete-modal-message');
    const listEl = document.getElementById('delete-modal-details');
    if (msgEl) msgEl.textContent = message || '¿Eliminar?';
    if (listEl) {
        listEl.innerHTML = '';
        (details || []).forEach(d => { const li = document.createElement('li'); li.textContent = d; listEl.appendChild(li); });
    }
    window._pendingDeleteCallback = onConfirm;
    const btn = document.getElementById('delete-confirm-btn');
    if (btn) btn.onclick = () => { if (window._pendingDeleteCallback) window._pendingDeleteCallback(); };
    openModal(modalId);
}

function closeDeleteConfirm() {
    closeModal('modal-delete-confirm');
    window._pendingDeleteCallback = null;
    const listEl = document.getElementById('delete-modal-details'); if (listEl) listEl.innerHTML = '';
}

function cancelDelete() {
    closeDeleteConfirm();
}

// ASSIGN modal helpers
function openAssignModal(section, targetId) {
    const modalId = 'modal-assign';
    const titleEl = document.getElementById('assign-modal-target');
    const select = document.getElementById('assign-employee-select');
    const dateInp = document.getElementById('assign-date');
    if (titleEl) titleEl.textContent = `Asignar responsable para ${section} ID: ${targetId}`;
    if (select) {
        select.innerHTML = '<option value="">-- seleccionar empleado --</option>';
        fetch('/api/empleados').then(r => r.json()).then(list => {
            window._employeesCache = list || [];
            (list || []).forEach(emp => {
                const opt = document.createElement('option');
                opt.value = emp.identificacion;
                opt.textContent = `${emp.nombre} (${emp.identificacion})`;
                select.appendChild(opt);
            });
            // after loading employees, load existing assignments for this target
            loadCurrentAssignments(section, targetId);
        }).catch(e => { console.error(e); loadCurrentAssignments(section, targetId); });
    }
    if (dateInp) dateInp.value = new Date().toISOString().slice(0,10);
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.dataset.targetSection = section;
        modal.dataset.targetId = String(targetId);
    }
    openModal(modalId);
}

function closeAssignModal() {
    const modal = document.getElementById('modal-assign');
    if (modal) {
        modal.dataset.targetSection = '';
        modal.dataset.targetId = '';
    }
    document.getElementById('assign-employee-select').innerHTML = '';
    document.getElementById('assign-date').value = '';
    closeModal('modal-assign');
}

async function saveAssign() {
    const modal = document.getElementById('modal-assign');
    if (!modal) return;
    const section = modal.dataset.targetSection;
    const targetId = modal.dataset.targetId;
    const select = document.getElementById('assign-employee-select');
    const dateVal = document.getElementById('assign-date').value;
    const empId = select ? select.value : '';
    if (!empId) { showModalError('assign','Selecciona un empleado'); return; }
    if (!dateVal) { showModalError('assign','Fecha requerida'); return; }

    try {
        let endpoint = '';
        let payload = { identificacion: empId, asignacion_fecha: dateVal };
        if (section === 'animales') { endpoint = '/api/empleado_animal'; payload.id_animal = targetId; }
        else if (section === 'maquinaria') { endpoint = '/api/empleado_maquinaria'; payload.id_maquinaria = targetId; }
        else if (section === 'cultivos') { endpoint = '/api/empleado_cultivo'; payload.id_cultivo = targetId; }
        else { showModalError('assign','Sección no soportada'); return; }

        const resp = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        const res = await resp.json();
        if (!resp.ok || !res.ok) throw new Error(res.error || 'Error asignando');
        showModalSuccess('assign','Asignación creada');
        setTimeout(() => { closeAssignModal();
            // reload affected section
            if (section === 'animales') loadAnimales();
            if (section === 'maquinaria') loadMaquinaria();
            if (section === 'cultivos') loadCultivos();
        }, 600);
    } catch (err) {
        console.error(err);
        showModalError('assign','Error creando asignación');
    }
}

// Load and render current assignments for a given target
async function loadCurrentAssignments(section, targetId) {
    const listEl = document.getElementById('assign-current-list');
    if (!listEl) return;
    listEl.innerHTML = '<li>Cargando...</li>';
    try {
        let endpoint = '';
        if (section === 'animales') endpoint = '/api/empleado_animal';
        else if (section === 'maquinaria') endpoint = '/api/empleado_maquinaria';
        else if (section === 'cultivos') endpoint = '/api/empleado_cultivo';
        else { listEl.innerHTML = '<li>Sección no soportada</li>'; return; }

        const res = await fetch(endpoint);
        const items = await res.json();
        const filtered = (items || []).filter(it => {
            if (section === 'animales') return String(it.id_animal) === String(targetId);
            if (section === 'maquinaria') return String(it.id_maquinaria) === String(targetId);
            if (section === 'cultivos') return String(it.id_cultivo) === String(targetId);
            return false;
        });
        listEl.innerHTML = '';
        if (filtered.length === 0) {
            listEl.innerHTML = '<li>Sin asignaciones</li>';
            return;
        }

        filtered.forEach(it => {
            const li = document.createElement('li');
            const empId = it.identificacion;
            const empName = (window._employeesCache || []).find(e => e.identificacion === empId)?.nombre || empId;
            li.textContent = `${empName} (${empId}) - ${it.asignacion_fecha || ''}`;
            const btn = document.createElement('button'); btn.type = 'button'; btn.className = 'btn danger-btn'; btn.style.marginLeft = '8px'; btn.textContent = 'Quitar';
            btn.addEventListener('click', async () => {
                if (!confirm('Quitar asignación?')) return;
                try {
                    let delEndpoint = endpoint;
                    const payload = { identificacion: empId };
                    if (section === 'animales') payload.id_animal = it.id_animal;
                    if (section === 'maquinaria') payload.id_maquinaria = it.id_maquinaria;
                    if (section === 'cultivos') payload.id_cultivo = it.id_cultivo;
                    const dres = await fetch(delEndpoint, { method: 'DELETE', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
                    const j = await dres.json();
                    if (!dres.ok || !j.ok) throw new Error(j.error || 'Error');
                    showModalSuccess('assign','Asignación removida');
                    // refresh assignments and section
                    loadCurrentAssignments(section, targetId);
                    if (section === 'animales') loadAnimales();
                    if (section === 'maquinaria') loadMaquinaria();
                    if (section === 'cultivos') loadCultivos();
                } catch (err) {
                    console.error(err);
                    showModalError('assign','Error removiendo asignación');
                }
            });
            li.appendChild(btn);
            listEl.appendChild(li);
        });
    } catch (err) {
        console.error(err);
        listEl.innerHTML = '<li>Error cargando asignaciones</li>';
    }
}

// ---------- MAQUINARIA CRUD (prompt-based) ----------
// Modal-based maquinaria handlers
function openMaquinariaForm(existing) {
    const modalId = 'modal-maquinaria';
    openModal(modalId, '#maquinaria-nombre');
    document.getElementById('maquinaria-modal-title').textContent = existing ? 'Editar Maquinaria' : 'Nueva Maquinaria';
    document.getElementById('maquinaria-nombre').value = existing ? existing.nombre : '';
    document.getElementById('maquinaria-tipo').value = existing ? existing.tipo : '';
    document.getElementById('maquinaria-modelo').value = existing ? existing.modelo : '';
    document.getElementById('maquinaria-estado').value = existing ? existing.estado : 'DISPONIBLE';
    document.getElementById(modalId).dataset.editId = existing ? existing.id : '';
}

function closeMaquinariaForm() {
    document.getElementById('modal-maquinaria').dataset.editId = '';
    closeModal('modal-maquinaria');
}

async function saveMaquinaria() {
    const editId = document.getElementById('modal-maquinaria').dataset.editId;
    const payload = {
        nombre: document.getElementById('maquinaria-nombre').value,
        tipo: document.getElementById('maquinaria-tipo').value,
        modelo: document.getElementById('maquinaria-modelo').value,
        estado: document.getElementById('maquinaria-estado').value
    };
    try {
        if (editId) {
            await fetch(`/api/maquinaria/${editId}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        } else {
            await fetch('/api/maquinaria', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        }
        closeMaquinariaForm();
        loadMaquinaria();
    } catch (e) {
        showModalError('maquinaria','Error guardando maquinaria');
    }
}

async function edit_maquinaria(data) { openMaquinariaForm(data); }

async function delete_maquinaria(id) {
    if (!confirm('¿Eliminar maquinaria?')) return;
    try {
        const res = await fetch(`/api/maquinaria/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (!res.ok || !data.ok) {
            showModalError('maquinaria', data.error || 'Error eliminando maquinaria');
            return;
        }
        loadMaquinaria();
    } catch (e) {
        console.error(e);
        showModalError('maquinaria','Error eliminando maquinaria');
    }
}

// ---------- CLIENTES CRUD (modal) ----------
function openClienteForm(existing) {
    const modalId = 'modal-cliente';
    openModal(modalId, '#cliente-documento');
    document.getElementById('cliente-modal-title').textContent = existing ? 'Editar Cliente' : 'Nuevo Cliente';
    document.getElementById('cliente-documento').value = existing ? existing.documento : '';
    document.getElementById('cliente-documento').disabled = existing ? true : false;
    document.getElementById('cliente-nombre').value = existing ? existing.nombre : '';
    document.getElementById('cliente-direccion').value = existing ? existing.direccion : '';
    document.getElementById('cliente-telefono').value = existing ? existing.telefono : '';
    document.getElementById('cliente-email').value = existing ? existing.email : '';
    document.getElementById(modalId).dataset.editId = existing ? existing.documento : '';
}

function closeClienteForm() {
    document.getElementById('cliente-documento').disabled = false;
    document.getElementById('modal-cliente').dataset.editId = '';
    // Remover la clase que aumenta el z-index
    const clienteModal = document.getElementById('modal-cliente');
    if (clienteModal) {
        clienteModal.classList.remove('modal-top');
    }
    closeModal('modal-cliente');
}

async function saveCliente() {
    const editId = document.getElementById('modal-cliente').dataset.editId;
    const payload = {
        documento: document.getElementById('cliente-documento').value,
        nombre: document.getElementById('cliente-nombre').value,
        direccion: document.getElementById('cliente-direccion').value,
        telefono: document.getElementById('cliente-telefono').value,
        email: document.getElementById('cliente-email').value
    };
    // basic validation
    if (!payload.documento || payload.documento.trim() === '') { showModalError('cliente','Documento requerido'); return; }
    if (!payload.nombre || payload.nombre.trim() === '') { showModalError('cliente','Nombre requerido'); return; }
    if (payload.email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(payload.email)) { showModalError('cliente','Email inválido'); return; }

    try {
        if (editId) {
            await fetch(`/api/clientes/${editId}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        } else {
            await fetch('/api/clientes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        }
        showModalSuccess('cliente','Guardado correctamente');
        setTimeout(() => { 
            closeClienteForm(); 
            loadClientes();
            // Si el cliente fue creado desde venta, recargar la lista de clientes en el formulario
            const ventaClienteSelect = document.getElementById('venta-cliente');
            if (ventaClienteSelect) {
                fetch('/api/clientes').then(r => r.json()).then(list => {
                    window.clientesCache = list || [];
                    ventaClienteSelect.innerHTML = '<option value="">-- seleccionar --</option>';
                    (list || []).forEach(c => {
                        const opt = document.createElement('option');
                        opt.value = c.documento;
                        opt.textContent = c.nombre;
                        ventaClienteSelect.appendChild(opt);
                    });
                    // Seleccionar el cliente recién creado
                    ventaClienteSelect.value = payload.documento;
                }).catch(e => console.error('Error cargando clientes', e));
            }
        }, 700);
    } catch (e) {
        showModalError('cliente','Error guardando cliente');
    }
}

async function edit_clientes(data) { openClienteForm(data); }

async function delete_clientes(id) {
    if (!confirm('¿Eliminar cliente?')) return;
    try {
        const res = await fetch(`/api/clientes/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (!res.ok || !data.ok) {
            showModalError('cliente', data.error || 'Error eliminando cliente');
            return;
        }
        loadClientes();
    } catch (e) {
        console.error(e);
        showModalError('cliente','Error eliminando cliente');
    }
}

// ---------- RECURSOS CRUD (modal) ----------
function openRecursoForm(existing) {
    const modalId = 'modal-recurso';
    openModal(modalId, '#recurso-nombre');
    document.getElementById('recurso-modal-title').textContent = existing ? 'Editar Recurso' : 'Nuevo Recurso';
    document.getElementById('recurso-nombre').value = existing ? existing.nombre : '';
    document.getElementById('recurso-tipo').value = existing ? existing.tipo_recurso : '';
    document.getElementById('recurso-stock').value = existing ? existing.stock : 0;
    document.getElementById(modalId).dataset.editId = existing ? existing.id : '';
}

function closeRecursoForm() {
    document.getElementById('modal-recurso').dataset.editId = '';
    closeModal('modal-recurso');
}

async function saveRecurso() {
    const editId = document.getElementById('modal-recurso').dataset.editId;
    const payload = {
        nombre: document.getElementById('recurso-nombre').value,
        tipo_recurso: document.getElementById('recurso-tipo').value,
        stock: parseInt(document.getElementById('recurso-stock').value || '0')
    };
    // basic validation
    if (!payload.nombre || payload.nombre.trim() === '') { showModalError('recurso','Nombre requerido'); return; }
    if (isNaN(payload.stock) || payload.stock < 0) { showModalError('recurso','Stock inválido'); return; }

    try {
        if (editId) {
            await fetch(`/api/recursos/${editId}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        } else {
            await fetch('/api/recursos', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        }
        showModalSuccess('recurso','Guardado correctamente');
        setTimeout(() => { closeRecursoForm(); loadRecursos(); }, 700);
    } catch (e) {
        showModalError('recurso','Error guardando recurso');
    }
}

async function edit_recursos(data) { openRecursoForm(data); }

async function delete_recursos(id) {
    if (!confirm('¿Eliminar recurso?')) return;
    try {
        const res = await fetch(`/api/recursos/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (!res.ok || !data.ok) {
            showModalError('recurso', data.error || 'Error eliminando recurso');
            return;
        }
        loadRecursos();
    } catch (e) {
        console.error(e);
        showModalError('recurso','Error eliminando recurso');
    }
}

