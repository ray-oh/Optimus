#!/usr/bin/env python
# coding: utf-8

"""
Module:         browser.py
Description:    playwright browser automation
Created:        22 Sep 2023

Versions:
20230922        First creation
"""
import re
from playwright.sync_api import sync_playwright, expect
from passwords import retrieveHttpCredentials
from prefect import get_run_logger
logger = get_run_logger()
from config import log_space, RPABROWSER

class Browser:
    def __init__(self, **kwargs):
        self.playwright = None
        self.RPABROWSER = RPABROWSER
        self.browsertype = None
        self.browser = None
        self.context = None
        self.page = None
        self.domain = None
        self.http_credentials = {'username': '', 'password': ''}
        #if not 'url' in kwargs:
        #    self.url = None
        #else:
        #    self.url = url

    def initialize(self, **kwargs):
        from prefect import get_run_logger
        logger = get_run_logger()
        logger.warning(f'{log_space}initialize kwargs'+ str(kwargs) + ' RPABROWSER: ' + str(RPABROWSER))
        import traceback

        #global playwright
        default = {"headless":False, "slow_mo":500}
        if not "headless" in kwargs:    kwargs["headless"] = default["headless"]
        if not "slow_mo" in kwargs:     kwargs["slow_mo"] = default["slow_mo"]

        try:
            if self.playwright == None:
                self.playwright = sync_playwright().start()
                #http_credentials=retrieveHttpCredentials(url)
                #return playwright
                #if not "http_credentials" in kwargs: 
                #http_credentials=retrieveHttpCredentials(url)
                #self.context = self.new_context()
                #self.page = self.new_page()
                #self.context = self.context.set_extra_http_headers(http_credentials=retrieveHttpCredentials(url))
                #self.context = self.new_context(http_credentials=retrieveHttpCredentials(url))
                #self.page = self.new_page()

                if RPABROWSER == 1:
                    self.browser = self.new_browser(**kwargs)
                    logger.debug(log_space+'Playwright None | Browser Type name:'+self.browser.browser_type.name + '| connected:' + self.browser.is_connected().__str__() + '| context: ' + self.browser.contexts.__str__())
                    result = True
                elif RPABROWSER == 2:
                    self.context = self.new_browser(**kwargs)
                    logger.debug(log_space+'Playwright None | Browser Type name:'+ ' Persistent Browser ' + '| connected:' + 'Persistent browser' + '| context: ' + self.context.__str__())
                    result = True
            else:
                if RPABROWSER == 1:
                    logger.debug(log_space+'Playwright ' + str(self.playwright) + ' | Browser Type name:'+self.browser.browser_type.name + '| connected:' + self.browser.is_connected().__str__() + '| context: ' + self.browser.contexts.__str__())
                    if not self.browser.is_connected():
                        self.playwright = sync_playwright().start()                    
                        self.browser = self.new_browser(**kwargs)
                        logger.debug(log_space+'New Browser - Playwright ' + str(self.playwright) + ' | Browser Type name:'+self.browser.browser_type.name + '| connected:' + self.browser.is_connected().__str__() + '| context: ' + self.browser.contexts.__str__())
                    else:
                        self.page = self.new_page()
                        pass
                    result = False
                    pass
                elif RPABROWSER == 2:
                    pass

        except Exception as error:
            logger.error('{0}Initialization Error: {1} | {2}'.format(log_space, type(error).__name__, error))
            logger.debug(log_space+traceback.format_exc())
            result = False
        return result

    def new_browser(self, **kwargs): # headless=False, slow_mo=3500
        from prefect import get_run_logger
        logger = get_run_logger()

        #global browser
        chrome = self.playwright.chromium
        if RPABROWSER == 1:
            return chrome.launch(**kwargs) #headless=headless, slow_mo=slow_mo)            
        elif RPABROWSER == 2:
            import os
            app_data_path = os.getenv("LOCALAPPDATA")
            user_data_dir = os.path.join(app_data_path, 'Chromium\\User Data\\Default')
            #r'%USERPROFILE%\AppData\Local\Chromium\User Data'
            #'%USERPROFILE%\AppData\Local\ms-playwright'
            logger.warning(f'{log_space}Persistent context created')
            return chrome.launch_persistent_context(user_data_dir=user_data_dir, **kwargs) #headless=headless, slow_mo=slow_mo)            

    def new_context(self, **kwargs):
        #global context
        #print(kwargs)
        from prefect import get_run_logger
        logger = get_run_logger()
        if RPABROWSER == 2:
            logger.warning(f'{log_space}Reuse existing browser context RPABROWSER {RPABROWSER}')            
            return self.context
        else:
            logger.warning(f'{log_space}New browser context created RPABROWSER {RPABROWSER}')
            return self.browser.new_context(**kwargs)

    def cookies(self):
        return self.context.cookies()

    def new_page(self):
        #global page
        self.page = self.context.new_page()
        return self.page

    def close_browser(self):
        from prefect import get_run_logger
        logger = get_run_logger()
        if RPABROWSER == 1:
            self.browser.close()
            self.playwright.stop()    
            logger.warning(log_space+'Close Browser - Playwright ' + str(self.playwright) + ' | Browser Type name:'+self.browser.browser_type.name + '| connected:' + self.browser.is_connected().__str__() + '| context: ' + self.browser.contexts.__str__())
            self.__init__()
        elif RPABROWSER == 2:
            self.context.close()
            self.playwright.stop()    
            logger.warning(log_space+'Close Browser - Playwright ' + str(self.playwright) + ' | Browser Type name:'+ 'Persistent browser' + '| connected:' + 'Persistent browser' + '| context: ' + self.context.__str__())
            self.__init__()

    def page_goto(self, url, authentication=0):
        http_credentials=retrieveHttpCredentials(url)
        # launch new context and page if the url domain has changed
        # or if the username has changed
        #from passwords import domain
        #new_domain = domain(url)
        #if self.domain == new_domain:
        #print('password',self.http_credentials, http_credentials)
        if RPABROWSER == 1:
            if http_credentials['username']=='':
                if self.http_credentials != http_credentials:
                    status = 'changed_to_no_credentials'
                else:
                    status = 'no_credentials'
            elif self.http_credentials != http_credentials:
                status = 'changed_credentials'
            else:
                status = 'with_credentials'

            if self.page!=None:
                if status == 'no_credentials':
                    pass
                elif status=='with_credentials':
                    pass
                elif status=='changed_credentials' or status=='changed_to_no_credentials':
                    #if authentication!=0:
                    if self.page!=None:
                        self.page.close()
                    self.context = self.new_context(http_credentials=http_credentials)
                    self.page = self.new_page()
            else:   # self.page==None
                if status == 'no_credentials':
                    self.context = self.new_context(http_credentials=http_credentials) #no_credentials then username=''
                    self.page = self.new_page()
                else:
                    self.context = self.new_context(http_credentials=http_credentials)
                    self.page = self.new_page()
            self.http_credentials = http_credentials
            self.page.goto(url, wait_until="load") #|"domcontentloaded"|
            logger.debug(f'{log_space}loaded page')
        else:  # RPABROWSER == 2
            if self.page==None: self.page = self.new_page()
            self.page.goto(url, wait_until="load") #|"domcontentloaded"|
            logger.debug(f'{log_space}loaded page')

    def _locator(self, selector):
        # determine locator
        '''
        page.get_by_role() to locate by explicit and implicit accessibility attributes.
        page.get_by_text() to locate by text content.
        page.get_by_label() to locate a form control by associated label's text.
        page.get_by_placeholder() to locate an input by placeholder.
        page.get_by_alt_text() to locate an element, usually image, by its text alternative.
        page.get_by_title() to locate an element by its title attribute.
        page.get_by_test_id() to locate an element based on its data-testid attribute (other attributes can be configured).
        '''
        from prefect import get_run_logger
        logger = get_run_logger()
        #logger.debug(f'_locator count    {self.page.locator(selector).count()}')
        selector = str(selector).strip()
        import traceback

        locator_type = None
        for i in ['explicit_selectors','implicit_selectors',
                  'title_exact','id','class','name','attribute',
                  'text_content_exact',
                  'role','label','placeholder',
                  'title_fuzzy',
                  'text_content_fuzzy'
                  ]:
            #logger.error(log_space+'Locator index '+i.__str__())
            try:
                if i=='explicit_selectors':
                    if str(selector).startswith("text="): locator_type = 'xpath_css'
                    elif str(selector).startswith("xpath=") or str(selector).startswith("//") or str(selector).startswith(".."): locator_type = 'xpath_css'
                    elif str(selector).startswith("css="): locator_type = 'xpath_css'
                    elif str(selector).startswith("css="): locator_type = 'xpath_css'
                    # implicit
                    elif (str(selector).startswith("\"") and str(selector).endswith("\"")) \
                            or (str(selector).startswith("\'") and str(selector).endswith("\'")): locator_type = 'text_content_implicit'
                    elif str(selector).startswith("//") or str(selector).startswith(".."): locator_type = 'xpath_css'

                    if locator_type!=None:
                        break
                    else:         # Wait for the "DOMContentLoaded" event.
                        self.page.wait_for_load_state("domcontentloaded")
                        self.page.wait_for_load_state()
                        self.page.wait_for_load_state("networkidle")

                elif i=='implicit_selectors':
                    if self.page.locator(selector).count() > 0: locator_type = 'xpath_css'
                elif i=='title_exact':  # self.page.get_by_title(r"Service Portal - Service Portal ").count()))
                    if self.page.get_by_title(selector, exact=True).count() > 0: locator_type = 'title_exact'
                elif i=='title_fuzzy':
                    if self.page.get_by_title(selector).count() > 0: locator_type = 'title_fuzzy'                    
                    #if self.page.locator('//title[contains(text(),"{0}")]'.format(selector)).count() > 0: locator_type = 'title_fuzzy'            
                elif i=='text_content_exact': #self.page.get_by_text(r"Service Portal - Service Portal ").count()))
                    if self.page.get_by_text(selector, exact=True).count() > 0: locator_type = 'text_content_exact'
                elif i=='text_content_fuzzy':
                    if self.page.get_by_text(re.compile(selector, re.IGNORECASE)).count() > 0: locator_type = 'text_content_fuzzy'
                elif i=='role':          #page.get_by_role("button", name="Sign in")
                    if self.page.get_by_role(selector, exact=True).count() > 0: locator_type = 'role'
                elif i=='label':
                    if self.page.get_by_label(selector, exact=True).count() > 0: locator_type = 'label'
                elif i=='placeholder':
                    if self.page.get_by_placeholder(selector, exact=True).count() > 0: locator_type = 'placeholder'
                elif i=='id':
                    if self.page.locator('//*[@id="{0}"]'.format(selector)).count() > 0: locator_type = 'id'            
                elif i=='class':
                    if self.page.locator('//*[@class="{0}"]'.format(selector)).count() > 0: locator_type = 'class'            
                elif i=='name':
                    if self.page.locator('//*[@name="{0}"]'.format(selector)).count() > 0: locator_type = 'name'            
                elif i=='attribute':
                    if self.page.locator('//*[@*="{0}"]'.format(selector)).count() > 0: locator_type = 'attribute'                    
                else: pass
                if locator_type!=None: break
            except Exception as error:
                #logger.warning(log_space+'{0}_locator_type error case: {1} | type= {2} | error= {3}'.format(log_space, i,type(error).__name__, error))  #, traceback.format_exc()
                #locator_type = "error"
                pass
        logger.debug(f'{log_space}Locator:{selector}'+ f'| Type:{locator_type}'+ f'| Page:{self.page.title()}')           
        return locator_type

    def wait(self, millisec=15000, **kwargs):
        from prefect import get_run_logger
        import traceback
        logger = get_run_logger()
        #logger.debug(f"{log_space}wait keywords', millisec {millisec} | kwargs {kwargs.keys()}")
        try:
            if not "selector" in kwargs.keys():
                #_type = self._locator(kwargs["selector"])
                #logger.debug('{0}_locator  count {1}'.format(log_space, self.page.locator('//title[contains(text(),"{0}")]'.format(kwargs["selector"])).count()))            
                #_type = 'none'
                self.page.wait_for_timeout(millisec)
                return True
            else:
                selector = kwargs["selector"]

                import time
                t_end = time.time() + int(millisec/1000) # time in sec
                #logger.error('t_end:' + t_end.__str__())
                while time.time() < t_end:
                    element = self.findElement(selector)
                    if element==None:
                        time.sleep(1)      # in sec
                    else:
                        #logger.error('element not none:' + str(selector))
                        break
                if element==None:
                    return False
                else:
                    #element.click(**kwargs)
                    element.wait_for(timeout=millisec)
                    #logger.error('element not none and complete wait for:' + str(selector))                    
                    return True
        except Exception as error:
            logger.error(log_space+'WAIT Error: {0} | {1}'.format(type(error).__name__, error))
            logger.debug(log_space+traceback.format_exc())
            return False

    def read(self, xpath, timeout=3000):
        result = self.page.locator(f'xpath={xpath}').inner_text(timeout=timeout)
        print(result)
        return result
    

    def findElement(self, selector):
        from prefect import get_run_logger
        import traceback
        logger = get_run_logger()

        _type = self._locator(selector)
        #logger.debug(log_space+'========================== TYPE is {0} ==========='.format(_type))
        import re
        selector = str(selector).strip()
        if False: pass
        elif _type==None:
            locator = None
        elif 'text' in _type:
            if _type == 'text_content_implicit':
                # remove quotes
                if selector.startswith("\""):    selector = selector.strip('\"')
                elif selector.startswith("\'"):  selector = selector.strip('\'')
            if _type == 'text_content_exact':
                locator = self.page.get_by_text(selector, exact=True)
            else:  #elif _type == 'text_content_fuzzy':
                locator = self.page.get_by_text(re.compile(selector, re.IGNORECASE))
        elif 'xpath' in _type or 'undefined' in _type or _type=='error':       # xpath or css
            locator = self.page.locator(selector)  #.wait_for(timeout=millisec)        
        elif _type=='title_exact':
            locator = self.page.get_by_title(selector, exact=True)        
        elif _type=='title_fuzzy':
            #locator = self.page.locator('//title[contains(text(),"{0}")]'.format(selector))
            locator = self.page.get_by_title(selector)            
            #count = locator.count()
            #logger.debug(log_space+'==========================TYPE 2 !!!! {0} | {1}'.format(_type, count))
            #logger.debug(log_space+'==========================WAITED !!!! {0} | {1}'.format(_type, locator.is_visible()))
        elif 'role' in _type:
            locator = self.page.get_by_role(selector, exact=True)        
        elif 'label' in _type:
            locator = self.page.get_by_label(selector, exact=True)        
        elif 'placeholder' in _type:
            locator = self.page.get_by_placeholder(selector, exact=True)        
        elif _type == 'id':            
            locator = self.page.locator('//*[@id="{0}"]'.format(selector))            
        elif _type == 'class':
            locator = self.page.locator('//*[@class="{0}"]'.format(selector))            
        elif _type == 'name':
            locator = self.page.locator('//*[@name="{0}"]'.format(selector))            
        elif _type == 'attribute':
            locator = self.page.locator('//*[@*="{0}"]'.format(selector))            
        else:
            locator = None
            #logger.debug(log_space+'==========================WARNING')
        if locator == None: count=0
        else: count= locator.count()
        logger.debug(log_space+'findElement TYPE: {0} | LOCATOR: {1}| Count: {2}'.format(_type, selector, count))
        #for x in range(count-1):
        #     logger.error('inner text:'+locator.inner_text())
        #logger.error(log_space+'Inner Text:' + locator.first.inner_html())
        #locator.first.highlight()
        if locator == None:
            return locator
        else:
            return locator.first


    def click(self, selector, **kwargs):
        from prefect import get_run_logger
        import traceback
        logger = get_run_logger()

        #print(selector)        
        #print(kwargs)
        import traceback

        try:
            element = self.findElement(selector)
            if element==None:
                return False
            else:
                element.click(**kwargs)
                return True

        except Exception as error:
            #logger.debug('==========================ERROR')
            logger.error(log_space+'Click Error: {0} | {1}'.format(type(error).__name__, error))
            logger.debug(log_space+traceback.format_exc())            

        return False
        if kwargs == {}:
            self.page.locator(selector).click()
        else:
            self.page.locator(selector).click(**kwargs)

    def select_option(self, selector, value):
        self.page.locator(selector).select_option(value)        

    def download(self, text, save_as):
        # Start waiting for the download
        from pathlib import Path
        with self.page.expect_download() as download_info:
            # Perform the action that initiates download
            element = self.page.get_by_text(re.compile(f'{text}', re.IGNORECASE))
            #page.get_by_text("Export")
            #page.locator('text="Click here to download your data file."') #.get_by_text("Export")
            element.click()   
            download = download_info.value
        # Wait for the download process to complete and save the downloaded file somewhere
        filePath = Path(save_as)
        download.save_as(filePath)    

    def press(self, key):
        self.page.keyboard.press(key)  # "Control+A" "Shift+A" "ArrowLeft" "Backspace"
        # F1 - F12, Digit0- Digit9, KeyA- KeyZ, Backquote, Minus, Equal, Backslash, Backspace, Tab, Delete, Escape, ArrowDown, End, Enter, Home, Insert, PageDown, PageUp, ArrowRight, ArrowUp, etc.

    def input(self, selector, value):
        from prefect import get_run_logger
        import traceback
        logger = get_run_logger()

        #print(selector)        
        #print(kwargs)
        import traceback

        try:
            element = self.findElement(selector)
            if element==None:
                return False
            else:
                element.fill(value)
                return True

        except Exception as error:
            #logger.debug('==========================ERROR')
            logger.error(log_space+'Input Error: {0} | {1}'.format(type(error).__name__, error))
            logger.debug(log_space+traceback.format_exc())            

        return False
        #self.page.locator(locator).fill(value)        

    def type(self, keys):
        self.page.keyboard.type(keys) 

    def snap(self, **kwargs):
        #self.page.keyboard.type(keys)
        self.page.screenshot(**kwargs)



def test():
    url = "https://qliksense.eu.dior.fashion/sense/app/70c92b52-3e94-4802-994c-5cfdec371d4a/sheet/6299ee78-10be-4f89-b8a9-4746ff64f094/state/analysis/bookmark/e702c838-8bc9-40c9-b7bc-6277ac24646e"
    #r = Browser(headless=False, slow_mo=500)
    r = Browser()
    r.initialize(headless=False, slow_mo=500)
    r.page_goto(url, authentication=1)
    r.wait(60000, text='Data up to ')
    #print(r.cookies())
    print('wait 15 sec')
    result = r.read('//h2[@title]', 13000)

    # Disable touch
    r.click('//button[@title="Navigation"]')
    r.click('//div[@class="qs-toolbar__toggle-touch-switch"]')
    r.click('//button[text()="Continue"]')
    r.wait(60000, selector='//html[@class="touch-off"]')

    r.select_option('//select[@class="qui-select lui-select"]', "Local")

    # Download as
    #r.click('//h2[@title]', button="right")
    r.click('//h2[@title]', button="right")
    r.click('//span[@title="Download as..."]')
    r.click('text="Data"')
    r.download("Click here to download your data file.", "./test1.xlsx")

    r.wait()

    r.close_browser()

if __name__ == "__main__":
    test()
