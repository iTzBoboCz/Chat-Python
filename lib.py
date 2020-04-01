import hashlib

def hashPassword(self, password):
    # zašifrování
    hashedPassword = hashlib.sha256()

    # osolení
    hashedPassword.update(password[2:31].encode("utf-8"))

    # převedení na hexidecimální hodnotu
    hashedPassword = hashedPassword.hexdigest()

    return(hashedPassword)
