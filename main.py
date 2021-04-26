from scraper import Scraper
from processor import Processor
from generate_wordclouds import Clouds
from generate_graphs import Graphs



while True:
    user_input = str(input("Please input 'g' for the graphs or 'c' for word clouds, 'u'for scraper and database updates, 'q' to quit the program\n")).lower()

    if user_input == 'q':
        print('Quiting the program')
        break

    elif user_input =='u':

        my_scraper = Scraper()
        my_scraper.update_data()

        my_processor = Processor()
        my_processor.process_store_csv()

    elif user_input == 'g':
        my_graph = Graphs()
        my_graph.draw_years_graphs()

    elif user_input =='c':
        my_cloud = Clouds()

        my_cloud.make_years_clouds()
