from multiprocessing.spawn import import_main_path
from protein_scrape import MuscleAndStrength


if __name__ == "__main__":
    ms = MuscleAndStrength()
    get_page = ms.get_url(
        "https://www.muscleandstrength.com/store/category/protein/whey-protein-isolate.html"
    )
    results = ms.parse_results(get_page)
    print(results)
