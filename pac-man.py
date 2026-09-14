from src.Parsing.parse_config_file import ParseConfig

if __name__ == "__main__":
    try:
        ParseConfig().load_json
    except Exception as e:
        print(e)