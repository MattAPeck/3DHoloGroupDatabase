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
# TODO
#  ---------------------------------------------------------------------------------------------------------------------
#  Delete unneeded comments.
#  Delete code blocks that won't go into final product.
#  ---------------------------------------------------------------------------------------------------------------------
# Keep in mind that not all of what is currently in this program will be implemented.
# Some of this is more to demonstrate and test our connection to the database and make sure our SQL is working properly.


def prompt_add_data():
    # This is our GoogleMaps API, and the Key that we will use.
    # The googlemaps api is how we will be getting our establishment types for a specific address.
    gmaps = googlemaps.Client(key='AIzaSyD166DaA9hYm7HaES8a8OePA4R9htLSmWQ')
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

        datemodified = datetime.datetime.now()  # First data insert. DateModified/Created are done at same time.
        datecreated = datetime.datetime.now()

    # This loop is needed because our gmaps result actually gives us multiple 'types' that an establishment
    # is classified as, and this is how we make sure all of them are recorded in separate rows for our use.
        for types in rever_geocode_result[0]['types']:
            type = types
            name = place_detail['result']['name']
            Database.create_establishment(latitude, longitude, datemodified, name, type, datecreated, mostusedsentencehistoryid)


def prompt_update_data():
    # TODO This entire function will need to be automated, much in the way that the previous function is/was.
    #  For future automation we should probably follow the format from above. That's if we even need this at all.
    # coordinates = Database.get_coordinates()
    # for data in coordinates:
    latitude = input('Latitude of location: ')  # data[1]
    longitude = input('Longitude of location: ')  # data[0]
    datemodified = datetime.datetime.now()  # Stays the same.
    name = input('Enter Establishment Name: ')  # I don't think we need to use GoogleMaps for this but we might.
    type = input('Enter Establishment Type: ')  # Same here, we might need to use the same Googlemaps format.
    id = input('Enter EstablishmentId: ')  # If we implment this we DEFINITELY need to change this,
    # due the the new format in the database... unless we just use MostUsedSentenceHistoryId instead of establishmentId.
    # In that case we need to change the SQL in Database too.
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
        # return id


# This is the function that tells Python where to start working. It will compile all code above this,
# but it should only run what is below this.
if __name__ == "__main__":
    # For now I use a while loop to keep everything running while we test, but this will be removed once
    # full implementation is done.
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
