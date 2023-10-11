import schedule
from time import sleep

from application.asyncio_scarper import Scraper
from dump.dump import run_dump

if __name__ == '__main__':
    s = Scraper()

    s.run()
    # schedule.every().day.at('12:00').do(s.run)
    # schedule.every().day.at('00:00').do(run_dump)

    # while True:
    #     schedule.run_pending()
    #     sleep(1)
