import urllib.parse
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def courtCode(self, listControlString):
        first = listControlString.find('"') + 1
        last = listControlString.rfind('"')
        return listControlString[first: last]

    def addresses(self, sublect_id,  city, street=''):

        sublect_id = urllib.parse.quote(sublect_id.encode('cp1251'))
        city = urllib.parse.quote(city.encode('cp1251'))

        if (street==''):
            url = 'https://sudrf.ru/index.php?id=300&act=go_ms_search&searchtype=ms&var=true&ms_type=ms&court_subj=' + sublect_id + '&ms_city=' + city + '&ms_street='

        else:
            street = urllib.parse.quote(street.encode('cp1251'))
            url = 'https://sudrf.ru/index.php?id=300&act=go_ms_search&searchtype=ms&var=true&ms_type=ms&court_subj=' + sublect_id + '&ms_city=' + city + '&ms_street=' + street

        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        driver = webdriver.Chrome()
        driver.get(url)

        error = 0
        courts = []

        try:
            table = driver.find_element_by_class_name("msFullSearchResultTbl")
            elements = table.find_elements_by_tag_name('tr')

            for element in elements:
                if (element.get_attribute('class') == 'firstRow'):
                    continue

                court = element.find_element_by_tag_name('a')

                listControl = court.get_attribute('onclick')
                courtCode = self.courtCode(listControl)

                court.click()

                yandexMap = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ballon_yamap_name')))
                yandexMap.click()

                courtAdress = driver.find_element_by_class_name('ya_map_info')

                courts.append({'name': court.text, 'code': courtCode, 'address': courtAdress.text})

        except WebDriverException:
            error = 1
            courts = []
        finally:
            driver.close()
            return json.dumps({'error': error, 'courts': courts})

