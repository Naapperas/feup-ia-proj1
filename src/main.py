from models import parse_model, Establishment
from graph import parse_graph


def main():
    establishments = parse_model('./resources/establishments.csv',
                                 Establishment)
    matrix = parse_graph('./resources/distances.csv')

    print('Matrix', matrix)
    print('Establishments', list(map(str, establishments)))


if __name__ == '__main__':
    main()
