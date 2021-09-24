from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import time


class CommentCrawler(object):
    # 드라이버와 최대 대기 시간을 전달받아 크롤러 객체를 생성합니다.
    def __init__(self, driver, wait_time):
        self.driver = driver
        self.wait_time = wait_time

    # 해당 url로 이동합니다.
    def go_to_news(self, url):
        self.driver.get(url)

    # 뉴스의 댓글란으로 이동합니다.
    def go_to_comment_section(self):
        element = WebDriverWait(self.driver, self.wait_time).until(
            (
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="cbox_module"]/div[2]/div[9]/a')
                )
            )
        )
        element.click()

    # 뉴스 댓글을 작성일자가 오래된 순으로 정렬합니다.
    def sort_comment_by_ascending_date(self):
        element = WebDriverWait(self.driver, self.wait_time).until(
            (
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="cbox_module_wai_u_cbox_sort_option_tab5"]')
                )
            )
        )
        element.click()

    # 마지막 댓글까지 이동합니다.
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

    # 뉴스의 작성일자를 전처리합니다.
    def time_parser1(self, dt):
        d, noon, t = dt.split(" ")
        is_noon = noon == "오후"
        new_dt = d + " " + t
        new_dt = datetime.strptime(new_dt, "%Y.%m.%d. %H:%M")
        if is_noon:
            new_dt = new_dt.replace(hour=new_dt.timetuple().tm_hour + 12)
        timestamp = time.mktime(new_dt.timetuple())
        return timestamp

    # 댓글이 달린 시간을 전처리합니다.
    def time_parser2(self, dt):
        new_dt = datetime.strptime(dt, "%Y.%m.%d. %H:%M:%S").timetuple()
        timestamp = time.mktime(new_dt)
        return timestamp

    # 뉴스에 달린 댓글들의 정보를 수집해 반환합니다.
    def get_comments(self):
        comment_info = {}
        elements = self.driver.find_elements_by_xpath(
            '//*[@id="cbox_module_wai_u_cbox_content_wrap_tabpanel"]/ul/li/div[1]/div'
        )

        comment_info["news_title"] = self.driver.find_element_by_xpath(
            '//*[@id="articleTitle"]/a'
        ).text
        comment_info["upload_time"] = self.time_parser1(
            self.driver.find_element_by_xpath(
                '//*[@id="main_content"]/div[1]/div[2]/div/span[1]'
            ).text
        )
        comment_info["n_comment"] = n_comment = len(elements)
        comment_info["comments"] = {}
        comment_info["n_bad_comment"] = 0

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
                    comment_info["n_bad_comment"] += 1
                    continue

                comment_info["comments"][f"{i}"] = {}
                comment_info["comments"][f"{i}"]["date"] = self.time_parser2(date)
                comment_info["comments"][f"{i}"]["comment"] = comment
                comment_info["comments"][f"{i}"]["n_thump_up"] = thumb_ups
                comment_info["comments"][f"{i}"]["n_thump_down"] = thumb_downs

        return comment_info

    # 뉴스 기사의 주소들로부터 댓글 정보를 수집해 반환합니다.
    def get_comments_from_list(self, url_list):
        data = []
        for url in url_list:
            self.go_to_news(url)
            self.go_to_comment_section()
            self.sort_comment_by_ascending_date()
            self.go_to_the_bottom_of_the_comments()
            data.append(self.get_comments())
        return data
