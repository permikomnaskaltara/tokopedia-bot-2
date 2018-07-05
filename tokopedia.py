#!/usr/bin/env python3
'''
tokopedia auto promote bot
Developed by Antonius (Ringlayer)
@ringlayer
Site : www.ringlayer.net - www.ringlayer.com
Robotic - Open Source - Digital Electronic
'''
from selenium import webdriver
import signal
import os,sys, time, inspect
from random import randint
import codecs

'''
start global variables
'''
start_url = "https://m.tokopedia.com/login"
homepage = "https://www.tokopedia.com/manage-product-new.pl"
tokopedia_username = "?"
tokopedia_password =  "?"
jeda_waktu_klik_iklan_dalam_jam=1
acak_promo_perjam = "1"
list_nama_produk = []
current_num = 0
'''
eof global variables
'''

def scrapper_click_elem_by_innerhtml(browser, element_name, inner_html):
    try:
        js =  'var ar_data = document.getElementsByTagName("' + element_name + '");'
        js += "\n"
        js += "for (i = 0; i < ar_data.length; i ++) {"
        js += "\n"
        js +=   "if (ar_data[i].innerHTML == '" +  inner_html + "') {"
        js += "\n"
        js += "ar_data[i].click();"
        js += "\n"
        js +="}"
        js += "\n"
        js += "}"
        browser.execute_script(js)
        return browser
    except Exception as e:
        raise

def _init_tokopedia_browser(url):
    html_source = "error_mark"
    try:
        profile = webdriver.FirefoxProfile()
        profile.set_preference("dom.webnotifications.enabled", False)
        ua = scrapper_randomize_ua()
        profile.set_preference("general.useragent.override", ua)
        profile.update_preferences()
        try:
            browser = webdriver.Firefox(firefox_profile=profile, executable_path='c:\Windows\System32\geckodriver.exe')
        except:
            try:
                browser = webdriver.Firefox(firefox_profile=profile, executable_path=r'geckodriver.exe')
            except:
                browser = webdriver.Firefox(firefox_profile=profile)
                pass
            pass

        #browser = webdriver.Firefox(firefox_profile=profile)
        browser.get(url)
        while (len(html_source) < 100) or (html_source.find("</html>") == -1):
                html_source = browser.page_source
                time.sleep(0.3)
        return html_source, browser
    except Exception as e:
        print(e)
        print ("[-] exception :" + inspect.stack()[0][3])
        pass
        return "", browser

def _get_source_praload(browser):
    html_source = "?"
    try:
        html_source = browser.page_source
        while (len(html_source) < 100) or (html_source.find("</html>") == -1):
            html_source = browser.page_source
            time.sleep(0.1)
    except Exception as e:
        print(e)
        print ("[-] exception :" + inspect.stack()[0][3])
        pass
    return html_source


def _stop_browser(browser):
    try:
        browser.quit()
    except Exception as e:
        print(e)
        print ("[-] exception :" + inspect.stack()[0][3])
        pass

def _login_to_site(browser, html_source):
    retme = 1
    try:
        global tokopedia_username
        global tokopedia_password
        global start_url
        mark1 = 'Kata Sandi'
        mark2 = "Masuk | Tokopedia"
        html_source = _cek_kepenuhan_pengunjung(browser)
        if (html_source.find(mark1) != -1) and (html_source.find(mark2) != -1):
            print ("[+] not logged in ! logging in ...")
            time.sleep(1)
            uname = browser.find_element_by_name('email')
            uname.click()
            uname.clear()
            uname.send_keys(tokopedia_username)
            passbox = browser.find_element_by_name('password')
            passbox.click()
            passbox.clear()
            passbox.send_keys(tokopedia_password)
            #browser.execute_script("document.getElementById('email_btn').click();")
            loginbut = browser.find_element_by_tag_name("button")
            loginbut.click()
            _get_source_praload(browser)
            time.sleep(7)
            html_source = browser.page_source
            if (html_source.find(mark1) != -1) and (html_source.find(mark2) != -1):
                print ("[-] login gagal")
                retme = 0
            else:
                print ("[+] login berhasil")
                time.sleep(10)
    except Exception as e:
        print(e)
        print ("[-] exception :" + inspect.stack()[0][3])
        pass
    return browser, retme

def _sundul(browser):
    try:
        global acak_promo_perjam
        global current_num
        global list_nama_produk
        if acak_promo_perjam == "1":
            current_nama_prod_to_click = list_nama_produk[current_num]
            print ("[+] melakukan klik pada nama produk :" + current_nama_prod_to_click)
            current_num += 1
            scrapper_click_elem_by_innerhtml(browser, "a", current_nama_prod_to_click)
            time.sleep(8)
            _get_source_praload(browser)
            _cek_kepenuhan_pengunjung(browser)
            try:
                print ("[+] melakukan promo perjam untuk nama produk : " +  current_nama_prod_to_click)
                browser.execute_script("document.getElementById('dink-it').click();")
            except Exception as e:
                print ("[-] gagal melakukan promo untuk nama produk : " + current_nama_prod_to_click)
                print(e)
                pass
            _get_source_praload(browser)
            _cek_kepenuhan_pengunjung(browser)
            time.sleep(3)
        else:
            print ("[-] settingan anda tidak benar, acak_promo_perjam harus 1")
    except Exception as e:
         print(e)
         print ("[-] exception :" + inspect.stack()[0][3])
         pass
    return browser


def _cek_sesi_login_tokopedia(browser):
    try:
        global homepage
        logged_in = 1
        browser.execute_script("window.location.replace('" + homepage + "');")
        html_source = _get_source_praload(browser)
        html_source = _cek_kepenuhan_pengunjung(browser)
        time.sleep(5)
        mark1 = 'Masuk</button>'
        mark2 = "Daftar</a>"
        if (html_source.find(mark1) != -1) and (html_source.find(mark2) != -1):
            logged_in = 0
        return logged_in
        '''
        rand_sec = randint(10, 900)
        time.sleep(rand_sec)
        '''
    except Exception as e:
        print(e)
        print ("[-] exception :" + inspect.stack()[0][3])
        pass
    return browser

def _cek_kepenuhan_pengunjung(browser):
    try:
        mark_kepenuhan = "kepenuhan pengunjung"
        html_source = _get_source_praload(browser)
        while (html_source.find(mark_kepenuhan) != -1):
            time.sleep(5)
            browser.execute_script("window.location.replace('" + browser.current_url + "');")
            html_source = _get_source_praload(browser)
        return html_source
    except Exception as e:
        print(e)
        print ("[-] exception :" + inspect.stack()[0][3])
        pass

def read_uname_pass_from_cfg():
    try:
        global tokopedia_username
        global tokopedia_password
        global jeda_waktu_klik_iklan_dalam_jam
        global acak_promo_perjam
        #try
        fp = open("config.txt", "r")
        if fp:
            for line in fp:
                line = line.strip()
                if line.find("tokopedia_username") != -1:
                    tokopedia_username = line.replace("tokopedia_username=", "").strip()
                elif line.find("tokopedia_password") != -1:
                    tokopedia_password = line.replace("tokopedia_password=", "").strip()
                elif line.find("jeda_waktu_klik_iklan_dalam_jam") != -1:
                    jeda_waktu_klik_iklan_dalam_jam = int(line.replace("jeda_waktu_klik_iklan_dalam_jam=", "").strip())
                elif line.find("acak_promo_perjam") != -1:
                    jeda_waktu_klik_iklan_dalam_jam = line.replace("acak_promo_perjam=", "").strip()
            fp.close
    except Exception as e:
        print(e)
        print ("[-] exception :" + inspect.stack()[0][3])
        pass


def set_working_dir():
    try:
        current_dir = os.popen("cd").read()
        if current_dir.find("run") == -1:
            os.chdir("run")
        os.system("cd")

    except Exception as e:
        print(e)
        print ("[-] exception :" + inspect.stack()[0][3])
        pass

def scrapper_randomize_from_list(list_collections):
    selected_data = ""
    try:
        total = len(list_collections)
        rand_num = randint(0, total - 1)
        selected_data = list_collections[rand_num].strip()
        return selected_data
    except Exception as e:
        print(e)
        print ("[-] exception :" + inspect.stack()[0][3])
        pass

def scrapper_randomize_ua():
    try:
        selected_ua = "?"
        ua_lists = []
        ua_lists.append("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0")
        ua_lists.append("Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0")
        ua_lists.append("Mozilla/5.0 (Windows NT 6.1; rv:55.0) Gecko/20100101 Firefox/55.0")
        selected_ua = scrapper_randomize_from_list(ua_lists)
        return selected_ua
    except Exception as e:
        print(e)
        print ("[-] exception :" + inspect.stack()[0][3])
        pass


def _baca_config_promo():
    try:
        global acak_promo_perjam
        fp = open("nama_produk.txt", "r")
        if fp:
            for line in fp:
                print ("[+] appending to list :" + line)
                list_nama_produk.append(line.strip())
            fp.close()
        if acak_promo_perjam == "0":
        	print ("[+] promo tidak diacak")
        else:
            print ("[+] acak promo")
    except Exception as e:
        print(e)
        print ("[-] exception :" + inspect.stack()[0][3])
        pass

def _operasi_utama():
    try:
        global jeda_waktu_klik_iklan_dalam_jam
        global start_url
        global homepage
        logged_in = 0
        read_uname_pass_from_cfg()
        _baca_config_promo()
        html_source, browser = _init_tokopedia_browser(start_url)
        browser.set_window_position(0, 0)
        browser.set_window_size(1280, 650)
        retme = 0
        _cek_kepenuhan_pengunjung(browser)
        browser, retme = _login_to_site(browser, html_source)
        #browser.execute_script("window.scrollTo(0, 250)")
        while True:
            if retme == 1:
                print("[+] operasi dimulai")
                browser.get("https://www.tokopedia.com/manage-product-new.pl")
                #scrapper_click_elem_by_innerhtml(browser, "a", "Daftar Produk")
                _get_source_praload(browser)
                time.sleep(5)
                _cek_kepenuhan_pengunjung(browser)
                scrapper_click_elem_by_innerhtml(browser, "a", "80")
                _get_source_praload(browser)
                time.sleep(10)
                #https://www.tokopedia.com/manage-product-new.pl?nref=pdlstside
                _cek_kepenuhan_pengunjung(browser)
                browser = _sundul(browser)
                time.sleep(10)
                browser.execute_script("window.location.replace('" + homepage + "');")
                _get_source_praload(browser)
                _cek_kepenuhan_pengunjung(browser)
                print("[+] idle dalam jam :" + str(jeda_waktu_klik_iklan_dalam_jam) + " jam")
                print("[+] sleeping ...")
                sleep_time = int(jeda_waktu_klik_iklan_dalam_jam * 3600)
                i = 0
                while i < sleep_time:
                    time.sleep(1)
                    i+=1
                logged_in = _cek_sesi_login_tokopedia(browser)
                if logged_in == 0:
                    browser, retme = _login_to_site(browser, html_source)
                    time.sleep(3)
    except Exception as e:
        raise

if __name__ == "__main__":
    _operasi_utama()
