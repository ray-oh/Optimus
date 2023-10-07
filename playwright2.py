import re
import asyncio
from playwright.async_api import async_playwright, expect

async def run(playwright):
    webkit = playwright.chromium
    browser = await webkit.launch(headless=False, slow_mo=3500)
    context = await browser.new_context(http_credentials={'username': 'roh@christiandior.com', 'password': 'HongKong202307'})
    #context = await browser.new_context()
    page = await context.new_page()
    check_date = "https://qliksense.eu.dior.fashion/sense/app/70c92b52-3e94-4802-994c-5cfdec371d4a/sheet/976db29b-a1c1-4e57-8e8f-1cb03b7ccb39/state/analysis/bookmark/ccae87bc-07e6-4f29-b1d9-d65769af4d18"
    await page.goto("https://qliksense.eu.dior.fashion") 
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
asyncio.run(main())
#await main()