import Database
import datetime
import googlemaps
import geopy
from geopy.geocoders import Nominatim
from transformers import pipeline, set_seed

# This is our testing menu. I just use this format to test all of our programs with user_input
# until we know everything works, then we automate.
menu = '''\n Please Select what you would like to do.
1. Insert new data.
2. Update existing data.
3. Find Existing data.
4. Generate Sentences.
5. Insert Sentence to table.
6. Prints DateTime timestamp for testing purposes.
7. Exit.

Your Selection: '''
# TODO
#  ---------------------------------------------------------------------------------------------------------------------
#  Rethink Database relationship between MostUsedCommonSentenceHistory and Establishment.
#  Move MostUsedSentenceHistoryId in Establishment Table and removing EstablishmentId
#  Loop over MostUsedSentenceHistoryTable WHERE MostUsedSentenceHistoryId IS NOT IN Establishment(table)
#  Reconsider/look into Geopy for potential reliability issues.
#  Alternatively, find out how to get Establishment name out of GoogleMapsAPI.
#  Create/implement the database call we need to retrieve the Lng/Lat coordinates from MostUsedSentenceHistory.
#  Delete unneeded comments.
#  ---------------------------------------------------------------------------------------------------------------------
# Keep in mind that not all of what is currently in this program will be implemented.
# Some of this is more to demonstrate and test our connection to the database and make sure our SQL is working properly.


def prompt_add_data():
    # This is our GoogleMaps API, and the Key that we will use.
    # The googlemaps api is how we will be getting our establishment types for a specific address.
    gmaps = googlemaps.Client(key='AIzaSyD166DaA9hYm7HaES8a8OePA4R9htLSmWQ')
    latitude = 40.1384284  # Hardcoded for now, but pulling/looping from MostUsedSentencesHistory in future
    longitude = -88.2586279
    rever_geocode_result = gmaps.reverse_geocode((latitude, longitude))

    # The googlemaps API doesn't give us the actual name of whatever is located at an address,
    # so we need another API for that. We tried Geopy, but we are looking for alternatives.
    """locator = Nominatim(user_agent='myGeocoder')
    coordinates = '40.1419295, -88.2547879'
    location = locator.reverse(coordinates)
    name = location.address[0]"""
    name = 'Red Lobster' # Temporary hardcode, will use whatever new api/method for the name.

    # Since this is us inserting information about an establishment for the first time,
    # the datemodified and datecreated are both the same.
    datemodified = datetime.datetime.now()
    datecreated = datetime.datetime.now()

    # This loop is needed because our gmaps result actually gives us multiple 'types' that an establishment
    # is classified as, and this is how we make sure all of them are recorded in separate rows for our use.
    # It's more database calls, but that isn't a long process to begin with,
    # and one that is fixed with a possible implementation of a connection pool in the future.
    for types in rever_geocode_result[0]['types']:
        type = types
        Database.create_establishment(latitude, longitude, datemodified, name, type, datecreated)


def prompt_update_data():
    # TODO This entire function will need to be automated, much in the way that the previous function is/was.
    latitude = input('Latitude of location: ')
    longitude = input('Longitude of location: ')
    datemodified = datetime.datetime.now()
    name = input('Enter Establishment Name: ')
    type = input('Enter Establishment Type: ')
    id = input('Enter EstablishmentId: ')
    Database.update_establishment(latitude, longitude, datemodified, name, type, id)


# TODO Delete.
def prompt_find_data():
    name = input('Enter the name of your desired establishment: ')
    return name


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


# TODO Remove this, we don't need this anymore with how the database design plans have changed.
def prompt_add_sentence():
    establishmentType = Database.get_establishment_type()
    for type in establishmentType:
        type = type[1]
        if type == 'Retail':
            type = 1
            return type
        elif type == 'Grocery':
            type = 2
            return type
        elif type == 'Hardware':
            type = 3
            return type


# This is the function that tells Python where to start working. It will compile all code above this,
# but it should only run what is below this.
if __name__ == "__main__":
    # For now I use a while loop to keep everything running while we test, but this will be removed once
    # full implementation is done.
    while (user_input := input(menu)) != '7':

        if user_input == '1':
            prompt_add_data()

        elif user_input == '2':
            prompt_update_data()

        elif user_input == '3':
            name = prompt_find_data()
            establishment = Database.find_data(name)
            if establishment is not None:
                print(establishment)
            else:
                print('There is no data about an establishment with that name, please try again.')

        elif user_input == '4':
            sentence_generate()

        elif user_input == '5':
            sentence = sentence_generate()
            type = prompt_add_sentence()
            Database.create_sentence(sentence, type)

        elif user_input == '6':
            print(datetime.datetime.now())

        else:
            print('Please select from the available options. ')
