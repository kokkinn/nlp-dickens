from src.text_generator import TextGenerator


def main():
    url: str = "https://www.online-literature.com/dickens/2941/"
    while True:
        nodes_number_bc = input('How many nodes [1 - 20] would you like to display in a bar chart ?\n')
        if not nodes_number_bc.isdigit():
            continue
        nodes_number_bc = int(nodes_number_bc)
        if 1 <= nodes_number_bc <= 20:
            break

    while True:
        nodes_number_g = input('How many nodes [1 - 1000] would you like to display in a graph ?\n')
        if not nodes_number_g.isdigit():
            continue
        nodes_number_g = int(nodes_number_g)
        if 1 <= int(nodes_number_g) <= 1000:
            break

    while True:
        sentences_number = input('How many sentences [1 - 15] would you like generate ?\n')
        if not sentences_number.isdigit():
            continue
        sentences_number = int(sentences_number)
        if 1 <= int(sentences_number) <= 15:
            break

    tg1 = TextGenerator(url)
    tg1.write_data_to_file()
    tg1.get_graph_html(nodes_number_g)
    tg1.get_bar_chart_image(nodes_number_bc)
    tg1.generate_text(sentences_number)

    print('\nThank you, all the resulting data is stored into "results/"')


if __name__ == '__main__':
    main()
