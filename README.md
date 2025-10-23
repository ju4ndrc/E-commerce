# Proyecto Integrador - FastAPI

## 1. Objetivo del Proyecto
El objetivo de este proyecto es desarrollar un sistema integrador que permita gestionar **usuarios, clientes, productos y órdenes** mediante una API REST construida con FastAPI. El proyecto busca demostrar buenas prácticas, relaciones complejas entre modelos y permitir la retroalimentación de profesores para consolidar la experiencia de desarrollo.

---

## 2. Persistencia de Datos
Se utiliza **[SQLite/PostgreSQL/MySQL]** como motor de base de datos para garantizar la persistencia de la información.  

### Tablas principales:
- `Users`
- `Customers`
- `Products`
- `Orders`

### Relaciones:
- **1:1 → User - Customer**: cada usuario puede estar asociado a un cliente específico  
- **1:N → Customer - Orders**: un cliente puede tener muchas órdenes  
- **N:M → Orders - Products**: una orden puede tener varios productos y un producto puede estar en varias órdenes  



---

## 3. Endpoints y Operaciones HTTP

La API expone los siguientes endpoints demostrando las relaciones y operaciones CRUD:

| Endpoint | Método | Descripción | Relación |
|----------|--------|------------|----------|
| `/users/` | ![#61affe](https://via.placeholder.com/15/61affe/000000?text=+) `GET` | Lista todos los usuarios | N/A |
| `/users/` | ![#49cc90](https://via.placeholder.com/15/49cc90/000000?text=+) `POST` | Crea un nuevo usuario | N/A |
| `/users/{id}` | ![#fca130](https://via.placeholder.com/15/fca130/000000?text=+) `PATCH` | Actualiza datos de un usuario | N/A |
| `/auth/login` | ![#49cc90](https://via.placeholder.com/15/49cc90/000000?text=+) `POST` | Autenticación de usuario | N/A |
| `/products/` | ![#61affe](https://via.placeholder.com/15/61affe/000000?text=+) `GET` | Lista todos los productos | N:M con Orders |
| `/products/` | ![#49cc90](https://via.placeholder.com/15/49cc90/000000?text=+) `POST` | Crea un producto | N:M con Orders |
| `/customers/` | ![#61affe](https://via.placeholder.com/15/61affe/000000?text=+) `GET` | Lista todos los clientes | 1:1 con Users |
| `/customers/` | ![#49cc90](https://via.placeholder.com/15/49cc90/000000?text=+) `POST` | Crea un cliente | 1:1 con Users |
| `/orders/` | ![#61affe](https://via.placeholder.com/15/61affe/000000?text=+) `GET` | Lista todas las órdenes | 1:N con Customers, N:M con Products |
| `/orders/` | ![#49cc90](https://via.placeholder.com/15/49cc90/000000?text=+) `POST` | Crea una orden | 1:N con Customers, N:M con Products |
| `/orders/{id}` | ![#f93e3e](https://via.placeholder.com/15/f93e3e/000000?text=+) `DELETE` | Elimina una orden (soft delete) | 1:N con Customers, N:M con Products |



### 4.1 Diagrama de Clases
[Ver diagrama de clases](https://lucid.app/lucidchart/b0d28342-71f0-47c6-9509-c1c7bacc733f/edit?viewport_loc=-2268%2C-20%2C3438%2C1642%2C0_0&invitationId=inv_b1e82a85-7a6b-4df6-a051-0582c8853b06)
