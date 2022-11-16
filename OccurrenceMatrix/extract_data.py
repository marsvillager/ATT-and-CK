from classification.attack_classification import get_all_src
from match import get_stop_words

if __name__ == '__main__':
    file = open("description_data.txt", mode="w", encoding="utf-8")

    filer_list: list = ["(e.g.,", "(i.e.", "and/or"]
    stop_words_list: list[str] = get_stop_words("../resources/stop_en_words.txt") + filer_list

    count = 1 # count numbers, relationship?
    src = get_all_src()
    mitre_lists: list = src.query()
    for mitre_list in mitre_lists:
        if 'description' in mitre_list:
            count += 1
            # file.write(mitre_list['description'])
            description_list: list = mitre_list['description'].split(" ")
            print(description_list)
            for description in description_list:
                flag: bool = True
                for stop_words in stop_words_list:
                    # case insensitive
                    if description.upper() == stop_words.upper():
                        flag = False
                        break
                if flag:
                    file.write(description + " ")

    file.close()
    print(count)
    print("ok")
