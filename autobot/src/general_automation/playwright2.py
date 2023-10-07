import re
import asyncio
from playwright.async_api import async_playwright, expect
from passwords import retrieveHttpCredentials

async def run(playwright):
    webkit = playwright.chromium
    browser = await webkit.launch(headless=False, slow_mo=3500)
    url="https://qliksense.eu.dior.fashion"
    context = await browser.new_context(http_credentials=retrieveHttpCredentials(url))

    #context = await browser.new_context()
    page = await context.new_page()
    check_date = "https://qliksense.eu.dior.fashion/sense/app/70c92b52-3e94-4802-994c-5cfdec371d4a/sheet/976db29b-a1c1-4e57-8e8f-1cb03b7ccb39/state/analysis/bookmark/ccae87bc-07e6-4f29-b1d9-d65769af4d18"
    await page.goto(url) 
    #wait:30,hub-nav-button,logon_DCLICK
    #await expect('xpath=hub-nav-button').to_contain_text(re.compile(r"Data up to"), timeout=60000)    
    #await expect("xpath=//button").to_have_id("hub-nav-button")
    #await expect(page.locator("button")).to_have_id("hub-nav-button")
    await page.locator('xpath=//button[@id="hub-nav-button"]').wait_for()
    await page.goto(check_date)     
    #wait:180,//button[@title="Navigation"],raisePageError
    #await page.locator('xpath=//button[@title="Navigation"]').wait_for()
    

    #read:strSearch=//h2[@title]
    locator = page.locator('xpath=//h2[@title]')
    #await expect(locator).to_contain_text("substring")
    await expect(locator).to_contain_text(re.compile(r"Data up to"), timeout=60000)
    
    
    #result = await page.locator('xpath=//h2[@title]').all_text_contents()
    result = await page.locator('xpath=//h2[@title]').inner_text(timeout=30000)    
    print('result1',result)
    
    #//button[@title="Navigation"]
    await page.locator('xpath=//button[@title="Navigation"]').click()
    await page.locator('xpath=//div[@class="qs-toolbar__toggle-touch-switch"]').click()
    #//button[text()="Continue"]
    await page.locator('xpath=//button[text()="Continue"]').click()
    await page.locator('xpath=//html[@class="touch-off"]').wait_for()    
    
    await page.wait_for_timeout(1000)    
    
    url = "https://qliksense.eu.dior.fashion/sense/app/70c92b52-3e94-4802-994c-5cfdec371d4a/sheet/890ebf80-5c1d-45a0-8dad-a577e8fb1cb5/state/analysis/bookmark/3d06bf05-3ade-4b0b-b9a2-9a0fe0718264"
    url = "https://qliksense.eu.dior.fashion/sense/app/70c92b52-3e94-4802-994c-5cfdec371d4a/sheet/6299ee78-10be-4f89-b8a9-4746ff64f094/state/analysis/bookmark/e702c838-8bc9-40c9-b7bc-6277ac24646e"
    await page.goto(url)
    await page.locator('xpath=//h2[@title]').wait_for()
    
    #select:qui-select lui-select,Local    
    await page.locator('xpath=//select[@class="qui-select lui-select"]').select_option("Local")
    
    await page.locator('xpath=//h2[@title]').click(button="right")

    #Download as
    #locator = page.get_by_text("Download as")
    #await page.locator('xpath=//span[@title="Download as..."]').wait_for()    
    await page.locator('xpath=//span[@title="Download as..."]').click()
    element = page.locator('xpath=//span[@title="Data"]') #.get_by_text("Data")
    element = page.locator('text="Data"') #.get_by_text("Data")
    await element.click()

    # Start waiting for the download
    async with page.expect_download() as download_info:
        # Perform the action that initiates download
        #await page.get_by_text("Download file").click()
        #element = page.locator('xpath=//span[@title="Export"]') #.get_by_text("Export")
        element = page.locator('text="Click here to download your data file."') #.get_by_text("Export")
        await element.click()
        
    download = await download_info.value
    # Wait for the download process to complete and save the downloaded file somewhere
    #await download.save_as("/path/to/save/at/" + download.suggested_filename)    
    #await download.save_as("./" + download.suggested_filename)    
    await download.save_as("./test1.xlsx")    
    
    result = await page.locator('xpath=//h2[@title]').inner_text(timeout=30000)    
    print('result2',result)
    await page.wait_for_timeout(15000)    
    
    #await page.goto("https://okta.lvmh.com/")
    #await page.screenshot(path="screenshot.png")
    #await page.waitForTimeout(2000) # waits for 2 seconds    
    #await page.wait_for_function("() => window.x > 0")
    #await page.wait_for_function("waitForTimeout(2000)")
    #await page.wait_for_function("() => {const now = Date.now(); return now - start > 2000;}") 
    await page.wait_for_timeout(1000)
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)


playwright = None
browser = None
context = None
page = None
def initialize(**kwargs):
    global playwright
    playwright = sync_playwright().start()
    http_credentials=retrieveHttpCredentials(url)
    #return playwright
    #if not "http_credentials" in kwargs: 
    #http_credentials=retrieveHttpCredentials(url)
    new_browser(headless=False, slow_mo=3500)
    new_context(**kwargs)
    new_page()

def new_browser(headless=False, slow_mo=3500):
    global browser
    chrome = playwright.chromium
    browser = chrome.launch(headless=headless, slow_mo=slow_mo)

def new_context(**kwargs):
    global context
    #print(kwargs)
    context = browser.new_context(**kwargs)

def new_page():
    global page
    page = context.new_page()

def page_goto(url):
    page.goto(url) 

def close_browser():
    browser.close()
    playwright.stop()    

def test():
    asyncio.run(main())

def test2():
    from playwright.sync_api import sync_playwright

    browser = new_browser()
    context = new_context(browser)
    page = new_page(context)
    page_goto(page, "https://qliksense.eu.dior.fashion")
    page.wait_for_timeout(1000)
    close_browser(browser)

from playwright.sync_api import sync_playwright

def run(playwright):
    firefox = playwright.chromium #firefox
    browser = firefox.launch(headless=False, slow_mo=3500)
    page = browser.new_page()
    page.goto("https://google.com")
    browser.close()

class Browser:
    def __init__(self, **kwargs):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        if not 'url' in kwargs:
            self.url = None
        else:
            self.url = url
        #global playwright
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

    def new_browser(self, **kwargs): # headless=False, slow_mo=3500
        #global browser
        chrome = self.playwright.chromium
        return chrome.launch(**kwargs) #headless=headless, slow_mo=slow_mo)

    def new_context(self, **kwargs):
        #global context
        #print(kwargs)
        return self.browser.new_context(**kwargs)

    def cookies(self):
        return self.context.cookies()

    def new_page(self):
        #global page
        return self.context.new_page()

    def close_browser(self):
        self.browser.close()
        self.playwright.stop()    

    def page_goto(self, url, authentication=0):
        if self.page==None:
            self.context = self.new_context()
            self.page = self.new_page()
        if authentication!=0:
            if self.page!=None:
                self.page.close()
            self.context = self.new_context(http_credentials=retrieveHttpCredentials(url))
            self.page = self.new_page()
        self.page.goto(url) 

    def wait(self, millisec=1000, **kwargs):
        #print(kwargs)
        #page.get_by_role("button", name="Sign in")

        #page.wait_for_timeout(millisec)
        if "text" in kwargs.keys():
            #locater = f'xpath={kwargs["identifier"]}'
            #print(locater)
            element = self.page.get_by_text(re.compile(f'{kwargs["text"]}', re.IGNORECASE))
            #expect(element).to_be_visible()
            element.wait_for(timeout=millisec)
        elif "xpath" in kwargs.keys():
            locater = f'xpath={kwargs["xpath"]}'
            #print(locater)
            element = self.page.locator(locater)  #.wait_for(timeout=millisec)        
            #page.get_by_text(re.compile(f'{kwargs["text"]}', re.IGNORECASE))
            element.wait_for(timeout=millisec)
        elif "selector" in kwargs.keys():
            locater = f'{kwargs["selector"]}'
            #print(locater)
            element = self.page.locator(locater)  #.wait_for(timeout=millisec)        
            #page.get_by_text(re.compile(f'{kwargs["text"]}', re.IGNORECASE))
            element.wait_for(timeout=millisec)            
        else:
            self.page.wait_for_timeout(millisec)
            #page.locator(locater).wait_for(timeout=millisec)
        #await expect(locator).to_contain_text(re.compile(r"Data up to"), timeout=60000)

    def read(self, xpath, timeout=3000):
        result = self.page.locator(f'xpath={xpath}').inner_text(timeout=timeout)
        print(result)
        return result
    
    def click(self, selector, **kwargs):
        #print(selector)        
        #print(kwargs)
        self.page.locator(selector).click(**kwargs)
        return
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



url = "https://qliksense.eu.dior.fashion/sense/app/70c92b52-3e94-4802-994c-5cfdec371d4a/sheet/6299ee78-10be-4f89-b8a9-4746ff64f094/state/analysis/bookmark/e702c838-8bc9-40c9-b7bc-6277ac24646e"
#r = Browser(headless=False, slow_mo=500)
r = Browser()
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
exit()


#with sync_playwright() as playwright:
#playwright = sync_playwright().start()
#run(playwright)
#playwright.stop()

#await main()
#new_browser()
#new_context(http_credentials={'username': 'roh@christiandior.com', 'password': 'HongKong202307'})
#new_page()
url = "https://qliksense.eu.dior.fashion/sense/app/70c92b52-3e94-4802-994c-5cfdec371d4a/sheet/6299ee78-10be-4f89-b8a9-4746ff64f094/state/analysis/bookmark/e702c838-8bc9-40c9-b7bc-6277ac24646e"
initialize(url=url, headless=False, slow_mo=3500)
page_goto(url)
def wait(millisec=1000, **kwargs):
    print(kwargs)
    #page.get_by_role("button", name="Sign in")

    #page.wait_for_timeout(millisec)
    if "text" in kwargs.keys():
        #locater = f'xpath={kwargs["identifier"]}'
        #print(locater)
        element = page.get_by_text(re.compile(f'{kwargs["text"]}', re.IGNORECASE))
        #expect(element).to_be_visible()
        element.wait_for(timeout=millisec)
    elif "xpath" in kwargs.keys():
        locater = f'xpath={kwargs["xpath"]}'
        #print(locater)
        element = page.locator(locater)  #.wait_for(timeout=millisec)        
        #page.get_by_text(re.compile(f'{kwargs["text"]}', re.IGNORECASE))
        element.wait_for(timeout=millisec)
    else:
        page.wait_for_timeout(millisec)
        #page.locator(locater).wait_for(timeout=millisec)
    #await expect(locator).to_contain_text(re.compile(r"Data up to"), timeout=60000)


#wait(6000)

#wait(30000,identifier='//button[@id="hub-nav-button"]')
wait(30000,text='Data up to ')
print('wait 15 sec')
#wait(15000)





def read(xpath, timeout=3000):
    result = page.locator(f'xpath={xpath}').inner_text(timeout=timeout)
    print(result)
    return result

result = read('//h2[@title]', 13000)

#//button[@title="Navigation"]
page.locator('xpath=//button[@title="Navigation"]').click()
page.locator('xpath=//div[@class="qs-toolbar__toggle-touch-switch"]').click()
#//button[text()="Continue"]
page.locator('xpath=//button[text()="Continue"]').click()
#page.locator('xpath=//html[@class="touch-off"]').wait_for()    
wait(30000,xpath='//html[@class="touch-off"]')

page.locator('xpath=//select[@class="qui-select lui-select"]').select_option("Local")

page.locator('xpath=//h2[@title]').click(button="right")

#Download as
#locator = page.get_by_text("Download as")
#await page.locator('xpath=//span[@title="Download as..."]').wait_for()    
page.locator('xpath=//span[@title="Download as..."]').click()
#element = page.locator('xpath=//span[@title="Data"]') #.get_by_text("Data")
element = page.locator('text="Data"') #.get_by_text("Data")
element.click()

def download(text, save_as):
    # Start waiting for the download
    from pathlib import Path
    with page.expect_download() as download_info:
        # Perform the action that initiates download
        element = page.get_by_text(re.compile(f'{text}', re.IGNORECASE))
        #page.get_by_text("Export")
        #page.locator('text="Click here to download your data file."') #.get_by_text("Export")
        element.click()   
    download = download_info.value
    # Wait for the download process to complete and save the downloaded file somewhere
    filePath = Path(save_as)
    download.save_as(filePath)    

download("Click here to download your data file.", "./test1.xlsx")

wait()

close_browser()



