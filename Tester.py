from core.NewsExtractor import *

if __name__ == "__main__":
    news = NewsResources()

    results = news.SkySport()
    for i in results:
        print(i)
