
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto("https://www.drushim.co.il/jobs/cat1/?q=python+developer")
    page.wait_for_selector(".job-header", timeout=10000)
    
    results = page.query_selector_all(".job-header")

    print(f"found {len(results)} jobs:")
    
    for i, job in enumerate(results[:10]):
        try:
            title = job.query_selector("span.job-url")
            company = job.query_selector("span.bidi")
            location = job.query_selector(".display-18")
            
            t = title.inner_text().strip() if title else "-"
            c = company.inner_text().strip() if company else "-"
            l = location.inner_text().strip() if location else "-"
            
            print(f"{i+1}. {t} | {c} | {l}")
        except:
            pass
    
    browser.close()

    