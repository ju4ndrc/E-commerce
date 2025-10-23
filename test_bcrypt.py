from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 👇 Copia el hash exactamente como aparece en tu base de datos:
hashed_pw = "$2b$12$rjHkTQId77tTnG5yhco0j.J35txB5HhcPLtGdNevVlVbteWKMGNLa"

# 👇 Escribe aquí la contraseña original que usaste al crear el usuario
plain_pw = "1234"

print(pwd_context.verify(plain_pw, hashed_pw))
