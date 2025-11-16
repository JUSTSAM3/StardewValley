
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
    } catch (error) {
        console.error(error);
        showError(section, "Error cargando sección " + section + ".");
    }
}

// UTILIDADES
function showError(section, msg) {
    const box = document.querySelector(`#section-${section} .section-content`);
    if (box) box.innerHTML = `<p style="color:red">${msg}</p>`;
}

function fillTable(section, headers, rows) {
    const box = document.querySelector(`#section-${section} .section-content`);
    if (!box) return;

    let html = "<table class='data-table'><thead><tr>";
    headers.forEach(h => html += `<th>${h}</th>`);
    html += "</tr></thead><tbody>";

    if (rows.length === 0) {
        html += `<tr><td colspan="${headers.length}">Sin datos</td></tr>`;
    } else {
        rows.forEach(r => {
            html += "<tr>";
            headers.forEach(h => {
                html += `<td>${r[h] ?? ""}</td>`;
            });
            html += "</tr>";
        });
    }

    html += "</tbody></table>";
    box.innerHTML = html;
}

// RESUMEN
async function loadResumen() {
    try {
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
    const res = await fetch("/api/animales");
    const data = await res.json();
    fillTable("animales", ["id", "nombre", "especie", "raza", "sexo", "estado"], data);
}

// CULTIVOS
async function loadCultivos() {
    const res = await fetch("/api/cultivos");
    const data = await res.json();
    fillTable("cultivos", ["id", "nombre", "tipo", "epoca", "estado", "fecha_siembra"], data);
}

// RECURSOS
async function loadRecursos() {
    const res = await fetch("/api/recursos");
    const data = await res.json();
    fillTable("recursos", ["id", "nombre", "tipo_recurso", "stock"], data);
}

// MAQUINARIA
async function loadMaquinaria() {
    const res = await fetch("/api/maquinaria");
    const data = await res.json();
    fillTable("maquinaria", ["id", "nombre", "tipo", "modelo", "estado"], data);
}

// EMPLEADOS
async function loadEmpleados() {
    const res = await fetch("/api/empleados");
    const data = await res.json();
    fillTable("empleados", ["identificacion", "nombre", "cargo", "fecha_ingreso", "sueldo"], data);
}

// PRODUCTOS
async function loadProductos() {
    const res = await fetch("/api/productos");
    const data = await res.json();
    fillTable("productos", ["identificacion", "nombre", "tipo", "precio"], data);
}

// CLIENTES
async function loadClientes() {
    const res = await fetch("/api/clientes");
    const data = await res.json();
    fillTable("clientes", ["documento", "nombre", "direccion", "telefono", "email"], data);
}

// VENTAS
async function loadVentas() {
    const res = await fetch("/api/ventas");
    const data = await res.json();
    fillTable("ventas", ["id", "cliente_nombre", "fecha", "total"], data);
}
