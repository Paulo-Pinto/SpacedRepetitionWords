from translate import Translator

translator = Translator(from_lang="de", to_lang="en")


def read_file():
    with open('words/german-word-list-' + 'nouns' + '.csv', encoding="utf-8") as fp:
        return list((x.split()[1]) for x in fp.readlines())[4:]


def write_file():
    with open('words/nouns', "w", encoding="utf-8") as fp:
        [fp.write(line + " " + translator.translate(str(line)).strip(".") + "\n") for line in read_file()]
        fp.close()


# for line in read_file():
#     print(line + " " + translator.translate(str(line)))

write_file()