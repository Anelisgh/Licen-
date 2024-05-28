from werkzeug.security import generate_password_hash

parola = "password"
parola_hash = generate_password_hash(parola)
print(parola_hash)
