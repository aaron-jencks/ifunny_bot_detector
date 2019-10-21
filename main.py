from ifunny_server import IFunnyServer
from reporter import Reporter
from tqdm import tqdm


def print_list(l: list):
    for li in l:
        print(li)


if __name__ == "__main__":
    print("Starting bot search")
    serv = IFunnyServer()
    rep = Reporter()

    while True:
        serv.page = 1
        serv.get_page()

        first = True
        while first or serv.next_page():
            if first:
                first = False

            print('Collecting page {}'.format(serv.page))
            serv.find_comments()
            print('Found {} comments'.format(len(serv.comments)))

            print('Looking for bots')
            bots = serv.detect_bots()
            print('Found {} bots!'.format(len(bots)))
            print('Reporting...')

            for b in tqdm(bots):
                rep.report(b)


