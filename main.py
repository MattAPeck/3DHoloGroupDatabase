import Database
import datetime
import googlemaps
from transformers import pipeline, set_seed

# This is our testing menu. I just use this format to test all of our programs with user_input
# until we know everything works, then we automate.
menu = '''\n Please Select what you would like to do.
1. Insert new data.
2. Update existing data.
3. Generate Sentences and add to the table.
4. Prints DateTime timestamp for testing purposes.
5. Exit.

Your Selection: '''


def prompt_add_data():
    gmaps = googlemaps.Client(key=)
    MostUsedSentenceHistoryId = Database.get_mostusedid()
    for data in MostUsedSentenceHistoryId:
        print(data)  # For testing purposes. Remove upon full implementation.
        mostusedsentencehistoryid = data[0]  # The database call SQL puts the variables in this order.
        longitude = data[1]  # Any change there will break this code.
        latitude = data[2]
        rever_geocode_result = gmaps.reverse_geocode((latitude, longitude))

        if len(rever_geocode_result) == 0:
            continue
        else:
            place_id = rever_geocode_result[0]['place_id']
        place_detail = gmaps.place(place_id)

        datemodified = datetime.datetime.now()
        datecreated = datetime.datetime.now()

        for types in rever_geocode_result[0]['types']:
            type = types
            name = place_detail['result']['name']
            Database.create_establishment(latitude, longitude, datemodified, name, type, datecreated, mostusedsentencehistoryid)


def prompt_update_data():
    latitude = input('Latitude of location: ')
    longitude = input('Longitude of location: ')
    datemodified = datetime.datetime.now()
    name = input('Enter Establishment Name: ')
    type = input('Enter Establishment Type: ')
    id = input('Enter EstablishmentId: ')
    Database.update_establishment(latitude, longitude, datemodified, name, type, id)


def sentence_generate():
    establishments = Database.get_establishment_type()
    for type in establishments:
        Id = type[0]
        type = type[1]
        generator = pipeline('text-generation', model='gpt2')
        set_seed(42)
        sentences = generator(f'Generate a sentence that someone would say in a {type} store if they are shopping there.',
                          max_length= 50, num_return_sequences=1)
        generated_text_list = [item['generated_text'] for item in sentences]
        for text in generated_text_list:
            Database.create_sentence(text, Id)

if __name__ == "__main__":
    while (user_input := input(menu)) != '5':

        if user_input == '1':
            prompt_add_data()

        elif user_input == '2':
            prompt_update_data()

        elif user_input == '3':
            sentence_generate()

        elif user_input == '4':
            print(datetime.datetime.now())

        else:
            print('Please select from the available options. ')
