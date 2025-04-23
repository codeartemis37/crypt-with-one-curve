import numpy as np
import lzma
import base64
import matplotlib.pyplot as plt

def compress_and_encode_key(key: str) -> str:
    compressed = lzma.compress(key.encode('utf-8'))
    b64 = base64.b64encode(compressed).decode('utf-8')
    return b64

def decode_and_decompress_key(b64key: str) -> str:
    compressed = base64.b64decode(b64key.encode('utf-8'))
    key = lzma.decompress(compressed).decode('utf-8')
    return key

def key_to_seed(key: str) -> int:
    return sum(ord(c) for c in key)

def generate_curve(key: str):
    np.random.seed(key_to_seed(key))
    return np.random.permutation(26)

def lettre_to_abs(lettre: str) -> int:
    return ord(lettre.upper()) - ord('A')

def abs_to_lettre(abs: int, maj: bool) -> str:
    base = ord('A') if maj else ord('a')
    return chr(base + abs)

def chiffre_texte(texte: str, key: str) -> str:
    courbe = generate_curve(key)
    res = []
    for c in texte:
        if c.isalpha():
            abs_c = lettre_to_abs(c)
            ordonnee = courbe[abs_c]
            res.append(abs_to_lettre(ordonnee, c.isupper()))
        else:
            res.append(c)
    return ''.join(res)

def dechiffre_texte(texte_chiffre: str, key: str) -> str:
    courbe = generate_curve(key)
    inverse_courbe = np.argsort(courbe)
    res = []
    for c in texte_chiffre:
        if c.isalpha():
            ordonnee = lettre_to_abs(c)
            abs_c = inverse_courbe[ordonnee]
            res.append(abs_to_lettre(abs_c, c.isupper()))
        else:
            res.append(c)
    return ''.join(res)

def affiche_courbe(courbe):
    x = np.arange(26)
    y = courbe
    lettres = [chr(ord('A') + i) for i in range(26)]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, '-o', label="Permutation de la clé")
    plt.scatter(x, y, color='red')

    # Annoter chaque point avec la lettre et les coordonnées
    for xi, yi, lettre in zip(x, y, lettres):
        plt.annotate(f"{lettre}:({xi},{yi})", (xi, yi), textcoords="offset points", xytext=(0,8), ha='center', fontsize=8)

    plt.title("Courbe de permutation des lettres (clé)")
    plt.xlabel("Abscisse (Lettre d'origine, A=0, B=1, ...)")
    plt.ylabel("Ordonnée (Lettre chiffrée, A=0, ...)")
    plt.xticks(x, lettres)
    plt.yticks(x, lettres)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

def chiffrement():
    texte = input("Texte à chiffrer : ")
    key = input("Clé : ")
    b64key = compress_and_encode_key(key)
    courbe = generate_curve(key)
    texte_chiffre = chiffre_texte(texte, key)
    print("\nClé compressée et encodée :")
    print(b64key)
    print("Texte chiffré :")
    print(texte_chiffre)
    affiche_courbe(courbe)

def dechiffrement():
    texte_chiffre = input("Texte chiffré : ")
    b64key = input("Clé compressée et encodée : ")
    key = decode_and_decompress_key(b64key)
    texte_dechiffre = dechiffre_texte(texte_chiffre, key)
    print("\nClé retrouvée :", key)
    print("Texte déchiffré :")
    courbe = generate_curve(key)
    affiche_courbe(courbe)

def main():
    mode = input("Mode (chiffrement/dechiffrement) ? [c/d] : ").strip().lower()
    if mode == 'c':
        chiffrement()
    elif mode == 'd':
        dechiffrement()
    else:
        print("Choix invalide.")

if __name__ == "__main__":
    main()
