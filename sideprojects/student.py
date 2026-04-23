def main():
    cos=[]
    numar=int(input('numar:'))
    for i in range(numar):
        produs=get_produse()
        cos.append(produs)
    total=0
    p=1
    for i in range(len(cos)):
        total+=cos[i]["pret"] *(1-p*0.05)
        p+=1
    print(total)

def get_produse():
    return {
        'nume':input('nume:'),
        'pret':int(input('pret:'))
    }


if __name__=='__main__':
    main()
# 2. Cere datele mai multor angajați (nume, salariu, departament), calculează bonusul diferit per departament și returnează angajatul cu cel mai mare salariu final.
def main():
    bonusuri={}
    angajati = []
    while True:
        angajat=get_angajat()
        angajati.append(angajat)
        bonusuri[angajat['departament']]=int(input('ce bonus?'))
        if angajat['nume']=='exit':
            break
    salariu=0
    max=angajati[0]
    for i in range(len(angajati)):
        salariu+=angajati[angajat['salariu']]+bonusuri[angajat['departament']]


def get_angajat():
    return{
        'nume':input('nume'),
        'salariu':int(input('salariu')),
        'departament':input('departament')
        }


if __name__ == "__main__":
    main()
# 3. Construiește un sistem de parolare unde parola trebuie validată (minim 8 caractere, o cifră, o literă mare) — fiecare regulă verificată de funcția ei, combinate într-o funcție valideaza().
# 4. Cere tranzacțiile unui cont bancar (depuneri și retrageri), validează fiecare tranzacție și returnează istoricul doar al celor reușite cu balanța la fiecare pas.
# 5. Cere datele mai multor studenți cu 3 note fiecare, calculează media, aplică o funcție de rotunjire proprie și afișează clasamentul final.
# 6. Construiește un sistem de livrare unde prețul depinde de greutate, distanță și tip de livrare (normal/express) — fiecare factor calculat separat și combinat la final.
# 7. Cere un text și extrage toate emailurile valide din el — folosind funcții separate pentru split, validare format și afișare rezultate.
# 8. Construiește un joc de ghicit numărul unde dificultatea (intervalul și numărul de încercări) e aleasă de user — logica de joc separată complet de logica de input.
# 9. Cere comenzile unui restaurant (masă, produse, cantități), calculează nota de plată cu taxă și bacșiș opțional și afișează bonul formatat.
# 10. Construiește un sistem de tururi unde fiecare tur are participanți cu vârste, validezi că toți au vârsta minimă, calculezi prețul per grup cu discount pentru copii și afișezi confirmarea.
