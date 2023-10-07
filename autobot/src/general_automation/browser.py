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
from config import log_space

class Browser:
    def __init__(self, **kwargs):
        self.playwright = None
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
        logger.warning(f'{log_space}initialize kwargs'+ str(kwargs))
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
                self.browser = self.new_browser(**kwargs)
                #self.context = self.new_context()
                #self.page = self.new_page()
                #self.context = self.context.set_extra_http_headers(http_credentials=retrieveHttpCredentials(url))
                #self.context = self.new_context(http_credentials=retrieveHttpCredentials(url))
                #self.page = self.new_page()
                logger.debug(log_space+'Playwright None | Browser Type name:'+self.browser.browser_type.name + '| connected:' + self.browser.is_connected().__str__() + '| context: ' + self.browser.contexts.__str__())                
                result = True
            else:
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
        except Exception as error:
            logger.error('{0}Initialization Error: {1} | {2}'.format(log_space, type(error).__name__, error))
            logger.debug(log_space+traceback.format_exc())
            result = False
        return result

    def new_browser(self, **kwargs): # headless=False, slow_mo=3500
        #global browser
        chrome = self.playwright.chromium
        return chrome.launch(**kwargs) #headless=headless, slow_mo=slow_mo)

    def new_context(self, **kwargs):
        #global context
        #print(kwargs)
        from prefect import get_run_logger
        logger = get_run_logger()
        logger.warning(f'{log_space}New browser context created')
        return self.browser.new_context(**kwargs)

    def cookies(self):
        return self.context.cookies()

    def new_page(self):
        #global page
        return self.context.new_page()

    def close_browser(self):
        from prefect import get_run_logger
        logger = get_run_logger()
        self.browser.close()
        self.playwright.stop()    
        logger.warning(log_space+'Close Browser - Playwright ' + str(self.playwright) + ' | Browser Type name:'+self.browser.browser_type.name + '| connected:' + self.browser.is_connected().__str__() + '| context: ' + self.browser.contexts.__str__())
        self.__init__()

    def page_goto(self, url, authentication=0):
        http_credentials=retrieveHttpCredentials(url)
        # launch new context and page if the url domain has changed
        # or if the username has changed
        #from passwords import domain
        #new_domain = domain(url)
        #if self.domain == new_domain:
        #print('password',self.http_credentials, http_credentials)
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
        def try_catch(fn):
            try:
                result = fn
            except Exception as error:
                logger.debug(log_space+'{0}_locator Error: {1} | {2} | {3} | {4}'.format(log_space, fn.__name__, type(error).__name__, error, traceback.format_exc()))
                result = False
            return result

        locator_type = None
        for i in [1,2,3,4,5,6,7,8,9,10]:
            try:
                if i==1:
                    if False: pass
                    elif str(selector).startswith("text="):
                        #selector = str(selector).split("=")[1]   
                        #if (str(selector).startswith("\"") and str(selector).endswith("\"")) \
                        #    or (str(selector).startswith("\'") and str(selector).endswith("\'")): locator_type = 'text-exactmatch'
                        #elif str(selector).startswith("\/"): locator_type = 'text-javascript-regex'
                        #else: locator_type = 'text'
                        locator_type = 'xpath_css'
                    elif str(selector).startswith("xpath=") or str(selector).startswith("//") or str(selector).startswith(".."): locator_type = 'xpath_css'
                    elif str(selector).startswith("css="): locator_type = 'xpath_css'
                    elif str(selector).startswith("css="): locator_type = 'xpath_css'
                    # implicit
                    elif (str(selector).startswith("\"") and str(selector).endswith("\"")) \
                            or (str(selector).startswith("\'") and str(selector).endswith("\'")): locator_type = 'text-implicit'
                    elif str(selector).startswith("//") or str(selector).startswith(".."): locator_type = 'xpath_css'
                    if locator_type!=None: break

                    self.page.wait_for_load_state("domcontentloaded")
                    self.page.wait_for_load_state()
                    self.page.wait_for_load_state("networkidle")

                elif i==2:
                    if False: pass                    
                    elif self.page.locator(selector).count() > 0: locator_type = 'xpath_css'
                    if locator_type!=None: break
                elif i==3:
                    if False: pass                    
                    elif self.page.get_by_title(selector).count() > 0: locator_type = 'title'
                    if locator_type!=None: break
                elif i==4:
                    if False: pass                    
                    elif self.page.locator('//title[contains(text(),"{0}")]'.format(selector)).count() > 0: locator_type = 'title2'            
                    if locator_type!=None: break
                elif i==5:
                    if False: pass                    
                    elif self.page.get_by_text(selector).count() > 0: locator_type = 'text'
                    if locator_type!=None: break
                elif i==6:
                    if False: pass                    
                    elif self.page.get_by_role(selector).count() > 0: locator_type = 'role'
                    if locator_type!=None: break
                elif i==7:
                    if False: pass                    
                    elif self.page.get_by_label(selector).count() > 0: locator_type = 'label'
                    if locator_type!=None: break
                elif i==8:
                    if False: pass                    
                    elif self.page.get_by_placeholder(selector).count() > 0: locator_type = 'placeholder'
                    if locator_type!=None: break
                elif i==9:
                    if False: pass                    
                    elif self.page.locator('//*[@id="{0}"]'.format(selector)).count() > 0: locator_type = 'id'            
                    if locator_type!=None: break
                elif i==10:
                    if False: pass                    
                    elif self.page.locator('//*[@class="{0}"]'.format(selector)).count() > 0: locator_type = 'class'            
                    if locator_type!=None: break
                else:
                    pass

                if True: pass
                # explicit selector strategy
                elif str(selector).startswith("text="):
                    #selector = str(selector).split("=")[1]   
                    #if (str(selector).startswith("\"") and str(selector).endswith("\"")) \
                    #    or (str(selector).startswith("\'") and str(selector).endswith("\'")): locator_type = 'text-exactmatch'
                    #elif str(selector).startswith("\/"): locator_type = 'text-javascript-regex'
                    #else: locator_type = 'text'
                    locator_type = 'xpath_css'
                elif str(selector).startswith("xpath=") or str(selector).startswith("//") or str(selector).startswith(".."): locator_type = 'xpath_css'
                elif str(selector).startswith("css="): locator_type = 'xpath_css'
                elif str(selector).startswith("css="): locator_type = 'xpath_css'

                # implicit
                elif (str(selector).startswith("\"") and str(selector).endswith("\"")) \
                        or (str(selector).startswith("\'") and str(selector).endswith("\'")): locator_type = 'text-implicit'
                elif str(selector).startswith("//") or str(selector).startswith(".."): locator_type = 'xpath_css'

                elif try_catch(self.page.locator(selector).count() > 0): locator_type = 'xpath_css'
                elif try_catch(self.page.get_by_title(selector).count() > 0): locator_type = 'title'
                elif try_catch(self.page.locator('//title[contains(text(),"{0}")]'.format(selector)).count() > 0): locator_type = 'title2'            
                elif self.page.get_by_text(selector).count() > 0: locator_type = 'text'
                elif self.page.get_by_role(selector).count() > 0: locator_type = 'role'
                elif self.page.get_by_label(selector).count() > 0: locator_type = 'label'
                elif self.page.get_by_placeholder(selector).count() > 0: locator_type = 'placeholder'
                else: locator_type = "undefined"
            except Exception as error:
                logger.warning(log_space+'{0}_locator_type Error: case {1} | error type= {2} *** error= {3}'.format(log_space, i,type(error).__name__, error))  #, traceback.format_exc()
                #locator_type = "error"
        return locator_type

    def wait(self, millisec=15000, **kwargs):
        from prefect import get_run_logger
        import traceback
        logger = get_run_logger()

        #logger.debug(f"{log_space}wait keywords', millisec {millisec} | kwargs {kwargs.keys()}")
        #self.page.wait_for_timeout(millisec)
        # Wait for the "DOMContentLoaded" event.
        #page.get_by_role("button", name="Sign in")
        try:
            if "selector" in kwargs.keys():
                _type = self._locator(kwargs["selector"])

                logger.debug(f'{log_space}Locator:{kwargs["selector"]}'+ f'| Type:{_type}'+ f'| Page:{self.page.title()}')           
                #logger.debug('{0}_locator  count {1}'.format(log_space, self.page.locator('//title[contains(text(),"{0}")]'.format(kwargs["selector"])).count()))            
                #logger.debug('{0}_locator  getbytitle {1}'.format(log_space, self.page.get_by_title(r"Service Portal - Service Portal ").count()))             
                #logger.debug('{0}_locator  getbytext {1}'.format(log_space, self.page.get_by_text(r"Service Portal - Service Portal ").count()))            
                #logger.debug(f'{log_space}_locator  count {self.page.locator(kwargs["selector"]).count()}')
  
  
            else:
                _type = 'none'
                self.page.wait_for_timeout(millisec)
                return True
  
        except Exception as error:
            logger.debug(log_space+'Wait checks error msg: error name= {0} | error= {1} '.format(type(error).__name__, error)) #, traceback.format_exc()))

        #logger.debug(log_space+'=========== Wait return _type result= {0}'.format(_type))
        try:
            selector = kwargs["selector"]
            element = self.findElement(selector)
            if element==None:
                return False
            else:
                #element.click(**kwargs)
                element.wait_for(timeout=millisec)
                return True


            #page.wait_for_timeout(millisec)
            if False: pass
            elif "text" in kwargs.keys():
                #locater = f'xpath={kwargs["identifier"]}'
                #print(locater)
                element = self.page.get_by_text(re.compile(f'{kwargs["text"]}', re.IGNORECASE))
                #expect(element).to_be_visible()
                element.wait_for(timeout=millisec)
            elif "xpath" in kwargs.keys():
                locater = f'xpath={kwargs["xpath"]}'
                element = self.page.locator(locater)  #.wait_for(timeout=millisec)        
                element.wait_for(timeout=millisec)

            elif 'text' in _type:
                locater = f'{kwargs["selector"]}'
                if _type == 'text-implicit':
                    # remove quotes
                    if locater.startswith("\""):    locater = locater.strip('\"')
                    elif locater.startswith("\'"):  locater = locater.strip('\'')
                element = self.page.get_by_text(re.compile(locater, re.IGNORECASE))
                element.wait_for(timeout=millisec)
            elif 'xpath' in _type or 'undefined' in _type or _type=='error':       # xpath or css
                locater = f'{kwargs["selector"]}'
                element = self.page.locator(locater)  #.wait_for(timeout=millisec)        
                element.wait_for(timeout=millisec)
            elif _type=='title':
                locater = f'{kwargs["selector"]}'
                element = self.page.get_by_title(locater)        
                element.wait_for(timeout=millisec)
            elif _type=='title2':
                element = self.page.locator('//title[contains(text(),"{0}")]'.format(kwargs["selector"]))
                count = element.count()
                logger.debug('==========================TYPE 2 !!!! {0} | {1}'.format(_type, count))
                #locater = f'{kwargs["selector"]}'
                #element = self.page.locator('//title[contains(text(),"{0}")]'.format(locater))        
                element.wait_for(timeout=millisec)
                logger.debug('==========================WAITED !!!! {0} | {1}'.format(_type, element.is_visible()))
            elif 'text' in _type:
                locater = f'{kwargs["selector"]}'
                element = self.page.get_by_text(locater)        
                element.wait_for(timeout=millisec)
            elif 'role' in _type:
                locater = f'{kwargs["selector"]}'
                element = self.page.get_by_role(locater)        
                element.wait_for(timeout=millisec)
            elif 'label' in _type:
                locater = f'{kwargs["selector"]}'
                element = self.page.get_by_label(locater)        
                element.wait_for(timeout=millisec)
            elif 'placeholder' in _type:
                locater = f'{kwargs["selector"]}'
                element = self.page.get_by_placeholder(locater)        
                element.wait_for(timeout=millisec)
            elif _type=='none':
                self.page.wait_for_timeout(millisec)
            else:
                self.page.wait_for_timeout(millisec)
                logger.debug('==========================WARNING')                
                #page.locator(locater).wait_for(timeout=millisec)
            #await expect(locator).to_contain_text(re.compile(r"Data up to"), timeout=60000)
            return True
        except Exception as error:
            #logger.error(log_space+'==========================ERROR AT WAIT')
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
        elif 'text' in _type:
            if _type == 'text-implicit':
                # remove quotes
                if selector.startswith("\""):    selector = selector.strip('\"')
                elif selector.startswith("\'"):  selector = selector.strip('\'')
            locator = self.page.get_by_text(re.compile(selector, re.IGNORECASE))
        elif 'xpath' in _type or 'undefined' in _type or _type=='error':       # xpath or css
            locator = self.page.locator(selector)  #.wait_for(timeout=millisec)        
        elif _type=='title':
            locator = self.page.get_by_title(selector)        
        elif _type=='title2':
            locator = self.page.locator('//title[contains(text(),"{0}")]'.format(selector))
            count = locator.count()
            #logger.debug(log_space+'==========================TYPE 2 !!!! {0} | {1}'.format(_type, count))
            #logger.debug(log_space+'==========================WAITED !!!! {0} | {1}'.format(_type, locator.is_visible()))
        elif 'text' in _type:
            locator = self.page.get_by_text(selector)        
        elif 'role' in _type:
            locator = self.page.get_by_role(selector)        
        elif 'label' in _type:
            locator = self.page.get_by_label(selector)        
        elif 'placeholder' in _type:
            locator = self.page.get_by_placeholder(selector)        
        elif _type == 'id':            
            locator = self.page.locator('//*[@id="{0}"]'.format(selector))            
        elif _type == 'class':
            locator = self.page.locator('//*[@class="{0}"]'.format(selector))            
        elif _type=='none':
            locator = None
        else:
            locator = None
            #logger.debug(log_space+'==========================WARNING')
        if locator == None: count=0
        else: count= locator.count()
        logger.debug(log_space+'findElement TYPE: {0} | LOCATOR: {1}| Count: {2}'.format(_type, selector, count))
        return locator


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

    def input(self, locator, value):
        self.page.locator(locator).fill(value)        

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
