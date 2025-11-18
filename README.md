READ ME para repositorio de GitHub del proyecto Stardew Valley – Sistema de Gestión de Granja (Bases de Datos 1).

Incluye:
✔ Descripción del proyecto
✔ Objetivos
✔ Tecnologías utilizadas
✔ Estructura del repositorio
✔ Instalación
✔ Ejecución del frontend Flask
✔ Ejecución de la base de datos (PostgreSQL)
✔ Créditos y documentación entregable


 ⭐ Stardew Valley – Sistema de Gestión de Granja
 Proyecto Bases de Datos 1 – Universidad El Bosque
 Autor: Jonathan Barrera Fernández 
 Autor: Samuel Andrés Mesa Comas 
 Autor: Juan Felipe Valderrama Peñaloza 


 📌 Descripción del Proyecto
Este proyecto implementa un sistema de información para la gestión de una granja tipo Stardew Valley, integrando:

 Administración de empleados
 Control de animales y cultivos
 Manejo de recursos y consumos
 Registro de productos generados
 Gestión de clientes y ventas
 Dashboard y consulta de datos mediante interfaz web

El sistema incluye tanto la base de datos relacional completa (PostgreSQL) como una interfaz web en Flask que permite visualizar, consultar y administrar la información mediante operaciones CRUD.



 🎯 Objetivos del Proyecto

 Diseñar un Modelo Entidad-Relación (MER) en notación Crow’s Foot
 Construir un Modelo Relacional (MR) normalizado
 Implementar la base de datos en PostgreSQL
 Documentar el proceso completo (VM, SO, RDBMS, diccionario, álgebra relacional)
 Crear un frontend funcional con Flask que permita interacción con la base de datos



 🏗️ Tecnologías Utilizadas

| Componente           | Tecnología                        |
| -- |  |
| Sistema Operativo VM | Ubuntu Server 22.04 LTS           |
| RDBMS                | PostgreSQL 15                     |
| Lenguaje backend     | Python 3.10                       |
| Framework web        | Flask                             |
| Frontend             | HTML5, CSS3, JavaScript           |
| Diagramación         | PlantUML (MER y MR – Crow’s Foot) |
| Herramientas         | VirtualBox, Lucidchart, draw.io   |



 📁 Estructura del Repositorio

```
StardewValley/
│── app.py                    Aplicación Flask
│── schema.sql                Script SQL del modelo relacional
│── requirements.txt          Librerías necesarias
│── README.md                 Este archivo
│
├── templates/                HTML del frontend
│   ├── login.html
│   ├── admin.html
│   └── about.html
│
├── static/                   Archivos estáticos
│   ├── css/
│   ├── js/
│   └── img/
│
└── docs/                     Documentación del proyecto
    ├── 1. Propuesta - Proyecto Bases de Datos.pdf
    ├── 2. Supuestos - Proyecto Bases de Datos.pdf
    ├── 3. MER Crow’s Foot.png
    ├── 4. MR Crow’s Foot.png
    ├── 5. Diccionario de Datos.pdf
    ├── 6. Álgebra Relacional.pdf
    ├── 7. Selección de Sistema Operativo.pdf
    ├── 8. Implementación VM.pdf
    ├── 9. Selección RDBMS.pdf
    └── 10. Implementación RDBMS.pdf
```



 🛠️ Instalación

 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/JUSTSAM3/StardewValley
cd StardewValley
```

 2️⃣ Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
source venv/bin/activate    Linux / Mac
venv\Scripts\activate       Windows
```

 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```



 🗄️ Configuración de la Base de Datos (PostgreSQL)

 1️⃣ Crear base de datos

```bash
sudo -u postgres createdb stardew
```

 2️⃣ Crear usuario (si aplica)

```sql
CREATE USER stardew_admin WITH PASSWORD 'admin123';
ALTER DATABASE stardew OWNER TO stardew_admin;
```

 3️⃣ Importar el esquema

```bash
psql -U stardew_admin -d stardew -f schema.sql
```



 🚀 Ejecutar la Aplicación Flask

```bash
python app.py
```

 Acceder en el navegador:

```
http://127.0.0.1:5000
```



 🔑 Credenciales de Prueba

Usuario: admin
Contraseña: admin

(Estas credenciales existen solo para desarrollo. No usar en producción.)



 📘 Documentación del Proyecto

Todo el entregable del curso está disponible en la carpeta docs/, e incluye:

📄 Propuesta del Proyecto
📄 Supuestos
📄 Diccionario de Datos
📄 MER y MR (Crow’s Foot)
📄 10 Consultas de Álgebra Relacional
📄 Selección del Sistema Operativo
📄 Implementación de VM
📄 Selección del RDBMS
📄 Implementación del RDBMS



 🙌 Créditos

Proyecto desarrollado por Pescados Rabiosos
Universidad El Bosque – Bases de Datos 1 – 2025
Docente: Ing. Armando Ricardo Medina Nieto 



  ⭐ Si este proyecto te fue útil, deja una estrella en el repositorio ❤️
