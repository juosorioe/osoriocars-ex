 #####    #####    #####   ######    ######   #####     ####     ###    ######    #####   
### ###  ##   ##  ### ###   ##  ##     ##    ### ###   ##  ##   ## ##    ##  ##  ##   ##  
##   ##  ##       ##   ##   ##  ##     ##    ##   ##  ##       ##   ##   ##  ##  ##       
##   ##   #####   ##   ##   #####      ##    ##   ##  ##       ##   ##   #####    #####   
##   ##       ##  ##   ##   ## ##      ##    ##   ##  ##       #######   ## ##        ##  
### ###  ##   ##  ### ###   ## ##      ##    ### ###   ##  ##  ##   ##   ## ##   ##   ##  
 #####    #####    #####   #### ##   ######   #####     ####   ##   ##  #### ##   #####   
                                                                                         
### Descripción del proyecto
Osorio Cars es un sitio web para la gestión de servicios automotrices. Incluye funcionalidades como registro de usuarios, carrito de compras, aplicación de descuentos, y un panel de administración para gestionar usuarios, servicios y códigos de descuento.

### Usuarios predeterminados
- Admin: `admin` / Contraseña: `admin`
- Usuario: `Nelson` / Contraseña: `osoriocars`

### Estructura del sitio web

#### Inicio
- **Hero:** Slider con información y una card mostrando el último servicio creado.
- **Información sobre la empresa:** Detalles de la empresa.
- **Servicios:** Muestra todos los servicios y los últimos 3 servicios creados.
- **Mapa:** Muestra la dirección de la empresa.

#### Sobre
- **Información sobre la empresa:** Detalles sobre la empresa.
- **Últimos 3 servicios añadidos.**

#### Servicios
- **Servicios disponibles:** Lista de servicios ofrecidos.
- **Sección para añadir un servicio:** Aparece solo si el usuario tiene el rol de 'mecanico'.

#### Admin Dashboard
- **Gestión de usuarios:** Modificación y eliminación de usuarios.
- **Códigos de descuento:** Gestión de códigos de descuento.
- **Compras hechas en el sitio web:** Visualización de las compras realizadas.

#### Perfil
- **Modificar información:** El usuario puede actualizar su información.
- **Ver cargo y rol:** Muestra el rol del usuario.
- **Compras hechas:** Lista de compras realizadas por el usuario.

#### Carrito
- **Servicios en el carrito:** Muestra los servicios añadidos al carrito.
- **Compra de servicios:** Posibilidad de comprar los servicios en el carrito.
- **Código de descuento:** Opción para aplicar un código de descuento.

### Cómo usar el sitio web

1. **Registro:** Los nuevos usuarios pueden registrarse proporcionando su información básica.
2. **Inicio de sesión:** Los usuarios registrados pueden iniciar sesión.
3. **Navegación por el sitio:**
   - Visita la página de inicio para ver el slider, el ultimo servicio y la información sobre la empresa.
   - Accede a la página de servicios para ver todos los servicios disponibles.
   - Si eres un mecánico, añade nuevos servicios desde la página de servicios, si eres comprador añade servicios a tu carrito.
   - Gestiona usuarios y descuentos desde el Admin Dashboard (solo para administradores).
   - Actualiza tu perfil y ve tus compras desde la página de perfil.
   - Añade servicios al carrito y realiza compras aplicando códigos de descuento desde la página del carrito.
4. **Compras:** Añade servicios al carrito y procede al checkout para completar la compra.

### Configuración del proyecto

1. **Clona el repositorio usando GIT:**
   ```bash
   git clone https://github.com/juosorioe/osoriocars-ex/
   ```

1. **Instala los requerimientos:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Aplica las migraciones:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Ejecuta el servidor:**
   ```bash
   python manage.py runserver
   ```
