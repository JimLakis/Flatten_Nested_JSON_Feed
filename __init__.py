# Python v3.6
# April, 2019

import urllib.request
import ast


def get_json(url):
    """ Opening an HTTP connection to the desired site, retreiving the JSON information and returning the JSON object. """
    def open_connection(url):
        """ Opening an HTTP connection to the desired site and returning an HTTP object. """
        http_response_obj = urllib.request.urlopen(url)
        return http_response_obj
    
    def acquire_json(http_response_obj):
        """ Reading in the JSON information and returning a JSON object. """
        json_obj = http_response_obj.read().decode("utf-8")
        return json_obj
    
    print("Acquiring the JSON feed...\n")
    http_response_obj = open_connection(url)
    json_obj = acquire_json(http_response_obj)
    return json_obj


def replace_nulls(json_obj):
    """ Reading through the JSON object and replacing 'null' values with None. """
    json_obj = json_obj.replace(":null,", ":None,")
    return json_obj


def convert_json_instance_obj_to_dict(json_obj):
    """ Converts the serialized JSON to a dictionary. """
    entire_report_dictionary = ast.literal_eval(json_obj)
    print("JSON instance object converted to a dictionary.\n")
    return entire_report_dictionary


def extract_records(entire_report_dictionary):
    """ Extracts and returns a 'flattened' list of records, each element of the list is a dictionary representing one record """
    def extract_number_of_records(entire_report_dictionary):
        """ Extracts the number of records (ie quakes reported) """
        if 'count' in entire_report_dictionary['metadata']:
            number_of_records = entire_report_dictionary['metadata']['count']
        #print(f"number_of_records: {number_of_records}")
        return number_of_records

    def extract_flatten_records(entire_report_dictionary, number_of_records):
        """ Flatten each record of nested dictionaries and lists into one dictionary (a record), per each element of a list """
        list_records = []
        for i in range(number_of_records):
            dict_records = entire_report_dictionary['features'][i]['properties'] # assigned value is a dictionary, thus creating the temporary dictionary
            dict_records['id'] = entire_report_dictionary['features'][i]['id']
            dict_records['type'] = entire_report_dictionary['features'][i]['geometry']['type']
            dict_records['latitude'] = entire_report_dictionary['features'][i]['geometry']['coordinates'][0]
            dict_records['longitude'] = entire_report_dictionary['features'][i]['geometry']['coordinates'][1]
            list_records.append(dict_records)
            del dict_records
        return list_records

    number_of_records = extract_number_of_records(entire_report_dictionary)
    list_records = extract_flatten_records(entire_report_dictionary, number_of_records)
    return number_of_records, list_records


def main():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_month.geojson"
    json_obj = get_json(url)
    json_obj = replace_nulls(json_obj)
    entire_report_dictionary = convert_json_instance_obj_to_dict(json_obj)
    number_of_records, list_records = extract_records(entire_report_dictionary)[0], extract_records(entire_report_dictionary)[1]

    # Confirming the return values
    print(f"Number of records claimed in metadata: {number_of_records}")
    print(f"Number of records counted: {len(list_records)}")

  
if __name__ == "__main__":
    main()