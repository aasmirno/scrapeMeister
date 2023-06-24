import sys
import Scraper as sc

args = sys.argv[1:]
clist_scraper = sc.Scraper()
# search/sss?query=sailboat+-wanted+-sold
r_val = clist_scraper.get_html(args[0], args[1])
if(r_val != 0):
    print(r_val)
clist_scraper.get_results()


