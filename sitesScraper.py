from googleplaces import GooglePlaces, types, lang
import sys
import time
import csv

YOUR_API_KEY = 'AIzaSyAM22VZLdFEx4ssRf2Anuik8GpE8cQzVg8'




def getInfo(query_result, writer):
    for place in query_result.places:
        # Returned places from a query are place summaries.
        print(place.name)
        # print(place.geo_location)
        # print(place.place_id)

        # The following method has to make a further API call.
        place.get_details()
        # Referencing any of the attributes below, prior to making a call to
        # get_details() will raise a googleplaces.GooglePlacesAttributeError.
        # print place.details # A dict matching the JSON response from Google.
        print(place.local_phone_number)
        # print place.international_phone_number
        print(place.website)
        if(place.website == None):
            continue
        # print(place.url)
        data = {'name': place.name, 'URL': place.website, 'phone': place.local_phone_number}
        writer.writerow(data)


def main(searchTerm):
    google_places = GooglePlaces(YOUR_API_KEY)
    search = searchTerm
    query_result = google_places.text_search(search)
    fName = search + ".csv"


    csvFile = open(fName, 'w')
    fieldnames = ['name', 'URL', 'phone']
    writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
    writer.writeheader()


    getInfo(query_result, writer)

    while query_result.has_next_page_token:
        print("--------------retrieving more results--------------")
        time.sleep(3)
        query_result = google_places.text_search(pagetoken=query_result.next_page_token)
        getInfo(query_result, writer)

    csvFile.close()
    print("All done!")
    # if query_result.has_next_page_token:
    # #     query_result_next_page = google_places.nearby_search(
    # #             pagetoken=query_result.next_page_token)
    #     print(query_result.next_page_token)


if __name__ == "__main__":
    main(sys.argv[1])
