import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()


class CommentCrawler(object):
    def __init__(self, driver, wait_time):
        self.driver = driver
        self.wait_time = wait_time

    def go_to_news(self, url):
        self.driver.get(url)

    def go_to_comment_section(self):
        element = WebDriverWait(self.driver, self.wait_time).until(
            (
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="cbox_module"]/div[2]/div[9]/a')
                )
            )
        )
        element.click()

    def sort_comment_by_ascending_date(self):
        element = WebDriverWait(self.driver, self.wait_time).until(
            (
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="cbox_module_wai_u_cbox_sort_option_tab5"]')
                )
            )
        )
        element.click()

    def go_to_the_bottom_of_the_comments(self):
        while True:
            try:
                element = WebDriverWait(self.driver, self.wait_time).until(
                    (
                        EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="cbox_module"]/div[2]/div[9]/a')
                        )
                    )
                )
                element.click()
            except:
                break

    def get_comments(self):
        comment_info = {}
        elements = self.driver.find_elements_by_xpath(
            '//*[@id="cbox_module_wai_u_cbox_content_wrap_tabpanel"]/ul/li/div[1]/div'
        )

        comment_info["news_title"] = self.driver.find_element_by_xpath(
            '//*[@id="articleTitle"]/a'
        ).text
        comment_info["upload_time"] = self.driver.find_element_by_xpath(
            '//*[@id="main_content"]/div[1]/div[2]/div/span[1]'
        ).text
        comment_info["n_comment"] = n_comment = len(elements)
        comment_info["comments"] = {}
        comment_info['n_bad_comment'] = 0

        if n_comment:
            for i, element in enumerate(elements):
                try:
                    date = element.find_element_by_xpath("div[3]/span").text
                    comment = element.find_element_by_xpath("div[2]/span[1]").text
                    thumb_ups = element.find_element_by_xpath("div[4]/div/a[1]/em").text
                    thumb_downs = element.find_element_by_xpath(
                        "div[4]/div/a[2]/em"
                    ).text
                except:
                    comment_info['n_bad_comment'] += 1
                    continue

                comment_info["comments"][f"{i}"] = {}
                comment_info["comments"][f"{i}"]["date"] = date
                comment_info["comments"][f"{i}"]["comment"] = comment
                comment_info["comments"][f"{i}"]["n_thump_up"] = thumb_ups
                comment_info["comments"][f"{i}"]["n_thump_down"] = thumb_downs

        return comment_info


crawler = CommentCrawler(driver, 5)
crawler.go_to_news(
    "https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=101&oid=025&aid=0003136866"
)
crawler.go_to_comment_section()
crawler.sort_comment_by_ascending_date()
crawler.go_to_the_bottom_of_the_comments()
comment_info = crawler.get_comments()
print(comment_info)

