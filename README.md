# Proyecto Integrador - FastAPI

## 1. Descripcion del proyecto
El proyecto consiste en desarrollar una plataforma de comercio electrónico que permita a los usuarios registrarse, buscar productos, agregarlos al carrito y realizar compras de manera segura. La aplicación contará con un panel de administración para gestionar productos, usuarios y pedidos, asegurando una experiencia completa tanto para clientes como para administradores.

---
## 2. Objetivo general
Desarrollar una plataforma de comercio electrónico funcional y segura que facilite la compra y venta de productos, permitiendo la gestión  de inventario y pedidos.

---

## 2. Persistencia de Datos
Se utiliza **[SQLite]** como motor de base de datos para garantizar la persistencia de la información.  

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
| `/users/` | ![GET](https://img.shields.io/badge/GET-blue) | Lista todos los usuarios | N/A |
| `/users/` | ![POST](https://img.shields.io/badge/POST-green) | Crea un nuevo usuario | N/A |
| `/users/{id}` | ![PATCH](https://img.shields.io/badge/PATCH-orange) | Actualiza datos de un usuario | N/A |
| `/auth/login` | ![POST](https://img.shields.io/badge/POST-green) | Autenticación de usuario | N/A |
| `/products/` | ![GET](https://img.shields.io/badge/GET-blue) | Lista todos los productos | N:M con Orders |
| `/products/` | ![POST](https://img.shields.io/badge/POST-green) | Crea un producto | N:M con Orders |
| `/customers/` | ![GET](https://img.shields.io/badge/GET-blue) | Lista todos los clientes | 1:1 con Users |
| `/customers/` | ![POST](https://img.shields.io/badge/POST-green) | Crea un cliente | 1:1 con Users |
| `/orders/` | ![GET](https://img.shields.io/badge/GET-blue) | Lista todas las órdenes | 1:N con Customers, N:M con Products |
| `/orders/` | ![POST](https://img.shields.io/badge/POST-green) | Crea una orden | 1:N con Customers, N:M con Products |
| `/orders/{id}` | ![DELETE](https://img.shields.io/badge/DELETE-red) | Elimina una orden (soft delete) | 1:N con Customers, N:M con Products |



### 4.1 Diagrama de Clases
[Ver diagrama de clases](https://lucid.app/lucidchart/b0d28342-71f0-47c6-9509-c1c7bacc733f/edit?viewport_loc=-2268%2C-20%2C3438%2C1642%2C0_0&invitationId=inv_b1e82a85-7a6b-4df6-a051-0582c8853b06)
