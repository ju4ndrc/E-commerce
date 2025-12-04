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
#  API Endpoints

| Endpoint | Método | Descripción | Relación |
|----------|--------|------------|----------|
| `/users/` | ![GET](https://img.shields.io/badge/GET-blue) | Lista todos los usuarios | N/A |
| `/users/` | ![POST](https://img.shields.io/badge/POST-green) | Crea un nuevo usuario | N/A |
| `/users/{user_id}` | ![PATCH](https://img.shields.io/badge/PATCH-orange) | Actualiza datos de un usuario | N/A |
| `/users/{user_id}` | ![DELETE](https://img.shields.io/badge/DELETE-red) | Desactiva un usuario (soft delete) | N/A |
| `/users/reactivate/{user_id}` | ![PATCH](https://img.shields.io/badge/PATCH-orange) | Reactiva un usuario | N/A |
| `/auth/login` | ![POST](https://img.shields.io/badge/POST-green) | Autenticación de usuario | N/A |
| `/products/` | ![GET](https://img.shields.io/badge/GET-blue) | Lista todos los productos | N:M con Orders |
| `/products/` | ![POST](https://img.shields.io/badge/POST-green) | Crea un producto (admin) | N:M con Orders |
| `/products/{product_id}` | ![PATCH](https://img.shields.io/badge/PATCH-orange) | Actualiza un producto (admin) | N:M con Orders |
| `/products/{product_id}` | ![DELETE](https://img.shields.io/badge/DELETE-red) | Elimina un producto (admin) | N:M con Orders |
| `/cart/` | ![GET](https://img.shields.io/badge/GET-blue) | Obtener el carrito activo del usuario | 1:1 con Users |
| `/cart/add/{product_id}` | ![POST](https://img.shields.io/badge/POST-green) | Agrega un producto al carrito | 1:1 con Users, N:M con Products |
| `/cart/remove/{product_id}` | ![DELETE](https://img.shields.io/badge/DELETE-red) | Elimina un producto del carrito | 1:1 con Users, N:M con Products |
| `/cart/clear` | ![DELETE](https://img.shields.io/badge/DELETE-red) | Vacía el carrito completo | 1:1 con Users, N:M con Products |
| `/orders/checkout` | ![POST](https://img.shields.io/badge/POST-green) | Realiza checkout y crea una orden | 1:N con Users, N:M con Products |
| `/orders/` | ![GET](https://img.shields.io/badge/GET-blue) | Lista todas las órdenes | 1:N con Users, N:M con Products |
| `/orders/{order_id}` | ![DELETE](https://img.shields.io/badge/DELETE-red) | Elimina una orden (soft delete) | 1:N con Users, N:M con Products |
| `/customers/` | ![GET](https://img.shields.io/badge/GET-blue) | Lista todos los clientes | 1:1 con Users |
| `/customers/` | ![POST](https://img.shields.io/badge/POST-green) | Crea un cliente | 1:1 con Users |



### 4.1 Diagrama de Clases
[Ver diagrama de clases](https://lucid.app/lucidchart/b0d28342-71f0-47c6-9509-c1c7bacc733f/edit?viewport_loc=-2268%2C-20%2C3438%2C1642%2C0_0&invitationId=inv_b1e82a85-7a6b-4df6-a051-0582c8853b06)
### 4.2 Documentacion
https://drive.google.com/file/d/1nKqNKAjCRxQhQdILiXm0buQLc57wxJUU/view?usp=sharing
