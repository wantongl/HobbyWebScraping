# HobbyWebScraping
I enjoy hearing lightnovel stories, but I'm tired of copy and pasting them into a translator then click audio.
Which led to this small script made by using Python with libraries: requests, beautifulsoup4, selenium.
To automate actions like web scrapping information from lightnovel hosting websites,
and then input the text into a translator to run the audio.

To run Selenium you will need geckodriver.exe for firefox, or chrome's driver to chrome.
browser = webdriver.Firefox(executable_path = r'(PUT PATH TO DRIVER HERE)') # Need path to selenium's webdriver (firefox/chrome)

paramDict values can be change to fit your needs.

The method SoupParseContent() needs to be changed in order to parse correct story text depending on the website in the url.

Final note,
Selenium is a really powerful and useful library for automating tasks on browser, it was pretty fun to learn and use.