import re, argparse

def tokenize_text(text):
    symbols = r'(?:[()\.,‘“?¿!¡…;:])'
    decimal_pattern = r'(?:\d+(?:[.,])\d+)'
    date_pattern = r'(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
    hour_pattern = r'(?:\d{1,2}:\d{2})'
    spanish_month = r'(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)'
    spanish_date_pattern = rf'(?:\d{{1,2}}\s+de\s+{spanish_month}(?:\s+de\s+\d{{2,4}})?)'
    url_pattern = r'(?:http(?:s)?://\S+)'
    email_pattern = r'(?:\S+@\S+\.\S+)'
    username_pattern = r'@[\w_]+'
    hashtag_pattern = r'#[\w_]+'
    acronym_pattern = r'(?:[A-Z]+\.)+'
    emoji_pattern = r'[\U00010000-\U0010ffff]'
    treatment_pattern = r'(?<!\w)(?:Sr\.|Sra\.|Dr\.|Dra\.|D\.|Dª\.|Lic\.|Ing\.|Prof\.)\s?'
    name_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+\b'

    pattern = f"{url_pattern}|{email_pattern}|{spanish_date_pattern}|{date_pattern}|{hour_pattern}|{decimal_pattern}|{username_pattern}|{hashtag_pattern}|{acronym_pattern}|{emoji_pattern}|{treatment_pattern}|{name_pattern}|{symbols}|\\w+"
    return re.findall(pattern, text)

def main(input_file, output_file):
    # Leer el archivo de entrada
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    # Tokenizar el texto
    tokens = tokenize_text(text)
    print(tokens)

    # Guardar los tokens en el archivo de salida
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(tokens))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tokenizador para el español.")
    parser.add_argument("-i", "--input", required=True, help="Archivo de entrada para tokenizar.")
    parser.add_argument("-o", "--output", required=True, help="Archivo de salida para guardar los tokens.")
    args = parser.parse_args()

    main(args.input, args.output)
