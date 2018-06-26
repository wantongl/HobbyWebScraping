import requests                                                        # Accessing website pages
from bs4 import BeautifulSoup                                          # Use for parsing
from selenium import webdriver                                         # Use for running browser (firefox)
from selenium.webdriver.support.ui import Select                       # For drop down list selections
from selenium.webdriver.common.by import By                            # -|
from selenium.webdriver.support.ui import WebDriverWait                # Use for verifying translation is done
from selenium.webdriver.support import expected_conditions as EC       # -|

# Parameters
paramDict ={
    "url"                   :"https://www.uukanshu.com/b/71643/13015.html",
    "baseurl"               :"https://www.uukanshu.com",
    "lang"                  :"Chinese Simplified",
    "ChangeVoiceToMale"     :1,            # Optional, 0 to not change, 1 to change
    "translateLoop"         :5,            # Optional, 0 to not read next chapter, n > 0, to read n chapters
}

#Access Data/Content from these URL
class Parse:
    def __init__(self, link):                                               # Initialize .html .data .nextpage
        self.html = self.request(self, link).text                           # Show html source as text
        self.data = self.SoupParseContent(self, self.request(self, link))   # Show the content/story text
        self.nextpage = self.nexturl(self, self.request(self, link))        # Shows the URL to the next page/chapter

    @staticmethod
    def request(self, link):
        resp = requests.get(link)                                    # Access website with get request
        resp.raise_for_status()                                      # Check if get request worked/downloaded
        txt = resp.text                                              # Convert html code to text
        soup = BeautifulSoup(txt, "lxml")                            # Convert html text to soup object
        return soup

    @staticmethod
    def SoupParseContent(self, soupobj): #*** Need to modify parsing depending on website to get content/story
        # Parse Data/Content
        content = soupobj.find("div", id="contentbox")                  # Parsing the content/story in div id = contentbox
        ad = "(adsbygoogle = window.adsbygoogle || []).push({});"

        result = ""                                                    # Placeholder of content combined as string
        result += str(content.text).replace(ad, '').replace("\n", '').replace(" ", '').lstrip() #remove ad, \n, whitespace

        # Found out the website did a format change on how the chapter content is shown in html.
        # Below not needed anymore, but can be used on old chapters; use to combine .find_all("p") into string
        # Pcontent = content.find_all("p")                             # Parse all content with p tags (we only want this)
        # for x in range(len(Pcontent)):                               # Loop to iterate through pcontentbox list
        #     result += Pcontent[x].text + "\n"                        # Add/append text to result
        return result

    @staticmethod
    def nexturl(self, soupObj):                                        # Parse link to next page/chapter and return partial url
        result = soupObj.find("a", id="next")                          # Example "/b/("some numbers").html"
        return result["href"]


web = Parse(paramDict['url'])     # Initialize object

# Below here is map out to bing translator, anything else won't work.
browser = webdriver.Firefox(executable_path = r'(PUT PATH TO DRIVER HERE)') # Need path to selenium's webdriver (firefox/chrome)
browser.get("https://www.bing.com/translator")
browser.implicitly_wait(30)                     # Global wait, will produce exception if no element is found within 30 secs

# Webdriver Manipulation
#1. Select language to Simpified Chinese (what I wanted to listen to)
#Since it's a drop list selector with options select element will be use.

langSelect = Select(browser.find_element_by_id("t_sl"))                  # Select drop off list
langSelect.select_by_visible_text(paramDict['lang'])                     # Selecting based on text using variable lang
print("Language Selected: ", paramDict['lang'])                          # Output current task

#2. Input text to the text field on bing
def inputText(translateText):
    bingTextbox = browser.find_element_by_id("t_sv")
    bingTextbox.click()
    bingTextbox.send_keys(translateText)
    print("Input Text Completed")


inputText(web.data)


# 3. Change voice to male (optional), default is female if don't want male set flag to 0
#    Only need to be set/run once at the beginning
notSet = 1
if paramDict['ChangeVoiceToMale'] == notSet:

    (WebDriverWait(browser, 300).until(                                     # Wait for button to be clickable
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#t_inauoption"))      # Click Voice Drag Down Option Button
        )).click()

    (WebDriverWait(browser, 300).until(                                     # Wait for button to be clickable
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#t_genradio_M_0"))    # Click Male Voice radio button
        )).click()

    notSet = 0
    print("Voice Changed to Male Completed")


#4. Start audio translation
def playaudio():
    playButton = browser.find_element_by_id("t_srcplaycIcon")
    playButton.click()
    print("Starting Translate Audio: ")


playaudio()         # Run play audio


#5. Find out when translation/audio stop
def verifyAudioStop():

    WebDriverWait(browser, 300).until(                                         # Wait for element to appear
        EC.presence_of_element_located((By.CSS_SELECTOR, "#t_srcplaycIcon.audio.audiofocus"))
        )
    print("Audio Start")

    WebDriverWait(browser, 900).until(                                         # Wait for element to disappear
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "#t_srcplaycIcon.audio.audiofocus"))   # Invis is slow try to find a faster confirming method
        )

    print("Audio Stop")


verifyAudioStop()


#6. Clear text
def cleartext():
    (browser.find_element_by_id("t_edc")).click()
    print("Clear Text")


cleartext()


#7. Repeat: updateweb paste start verify clear loop for next chapter (optional)
for x in range(1, paramDict['translateLoop'] + 1):
    print("Next Chapter Translating: ")
    print("URL: ", paramDict['baseurl'] + web.nextpage)
    web = Parse(paramDict['baseurl'] + web.nextpage)
    inputText(web.data)
    playaudio()
    verifyAudioStop()
    cleartext()



