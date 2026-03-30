def main():
    cos=[]
    numar=int(input('numar:'))
    for i in range(numar):
        produs=get_produse()
        cos.append(produs)
    total=0
    for i in range(1,len(cos)):
        total+=cos[i]["pret"] - (cos[i]["pret"]*(100-i*5))/100

    print(total)

def get_produse():
    return {
        'nume':input('nume:'),
        'pret':int(input('pret:'))
    }


if __name__=='__main__':
    main()
