from crawler import CommentCrawler
from selenium import webdriver

if __name__ == '__main__':
    news_urls = ["https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=101&oid=025&aid=0003136866"]
    driver = webdriver.Chrome()
    crawler = CommentCrawler(driver, 5)
    comment_info = crawler.get_comments_from_list(news_urls)
    print(comment_info)


