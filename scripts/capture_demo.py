"""Read-only screenshots against the actual running local demonstration workspace."""
from pathlib import Path
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as pw:
        chrome=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
        browser=pw.chromium.launch(headless=True,executable_path=str(chrome) if chrome.exists() else None)
        page=browser.new_page(viewport={'width':1440,'height':1000})
        for target,title in [('overview','Voting intelligence'),('explorer','Notice explorer'),('performance','How much work can AI safely remove?'),('dataset','Dataset & methodology')]:
            page.goto(f'http://127.0.0.1:8000/#{target}')
            page.get_by_role('heading',name=title,exact=True).wait_for()
            page.screenshot(path=f'artifacts/demo-{target}.png',full_page=True)
        page.goto('http://127.0.0.1:8000/#overview')
        page.get_by_role('heading',name='Voting intelligence',exact=True).wait_for()
        page.get_by_role('checkbox',name='Demo mode').check()
        page.locator('[data-record="alpaca_corrective:3069"]').click()
        page.locator('.source-text').wait_for()
        page.screenshot(path='artifacts/demo-notice.png',full_page=True)
        browser.close()
if __name__=='__main__':main()
