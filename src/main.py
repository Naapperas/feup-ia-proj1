from models import parse_model, Establishment

def main():
    establishments = parse_model('./resources/establishments.csv', Establishment)

    print('Establishments', list(map(str, establishments)))

if __name__ == '__main__':
    main()