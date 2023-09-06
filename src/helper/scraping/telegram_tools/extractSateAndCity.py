from geosky import geo_plug
import pandas as pd

main_folder = '../../../../'
input_file_path = main_folder +'data/telegram/queries/DACH.txt'

def get_country_to_state_dict():
    # prepare country-states mapping
    data_state = geo_plug.all_Country_StateNames()
    data_state = data_state.replace('null', ' ')
    res = eval(data_state)

    mapping_state = {}
    for element in res:
        for k, v in element.items():
            mapping_state[k] = v
    # print(mapping_state['China'])  # e.g. {'':['Zurich', 'Zug', 'Vaud', 'Saint Gallen'...], '':[]}

    mapping_state["Switzerland"].remove("Basel-City")
    mapping_state["Switzerland"].append("Basel")

    return mapping_state

def get_state_to_city_dict():
    # prepare country-city mapping
    data_city = geo_plug.all_State_CityNames()
    data_city = data_city.replace('null', ' ')
    res = eval(data_city)

    mapping_city = {}
    for element in res:
        for k, v in element.items():
            mapping_city[k] = v
    mapping_city['North Rhine-Westphalia'].append('Cologne')
    mapping_city['Bavaria'].append('Nuremberg')
    mapping_city['Basel'] = mapping_city.pop('Basel-City')
    return mapping_city

def special_translate_chat(chat):
    return chat.replace("Lousanne", "Lausanne") \
                .replace("BielBienne", "Biel/Bienne")\
                .replace("Geneve", "Geneva") \
                .replace("StGallen", "Saint Gallen") \
                .replace("", "") \
                .replace("", "") \
                .replace("", "") \
                .replace("", "")

if __name__ == '__main__':

    mapping_state = get_country_to_state_dict()
    mapping_city = get_state_to_city_dict()

    countries, states, cities, chats = list(), list(), list(), list()
    with open(input_file_path, 'r') as file:
        for line in file.readlines():
            if line.startswith("#"):
                country = line.replace('#', '').replace('\n', '')
            else:
                chat = line.replace('\n', '')

                chat_standard = special_translate_chat(chat)

                # parse state and city
                chat_states = mapping_state[country]
                state, city = '', ''
                for s in chat_states:
                    chat_city = mapping_city[s]
                    for c in chat_city:
                        if c.upper() in chat_standard.upper():
                            city = c
                            state = s
                            break

                        if s.upper() in chat_standard.upper():
                            state = s

                chats.append(chat)
                countries.append(country)
                states.append(state)
                cities.append(city)

    # write csv
    df = pd.DataFrame(list(zip(countries, states, cities, chats)),
                      columns =['country', 'state', 'city', 'chat'])
    df.to_csv(main_folder+'data/telegram/queries/chat_with_country.csv', index=False)
