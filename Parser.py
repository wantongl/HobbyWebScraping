import requests                                                        # Accessing website pages
from bs4 import BeautifulSoup                                          # Use for parsing
from selenium import webdriver                                         # Use for running browser (firefox)
from selenium.webdriver.support.ui import Select                       # For drop down list selections
from selenium.webdriver.common.by import By                            # -|
from selenium.webdriver.support.ui import WebDriverWait                # Use for verifying translation is done
from selenium.webdriver.support import expected_conditions as EC       # -|

# Parameters
paramDict ={
    "fullchapterurl"        :"https://www.uukanshu.com/b/71643/13068.html",
    "baseurl"               :"https://www.uukanshu.com",
    "language"              :"Chinese Simplified",
    "webdriver"             :r"C:\Users\00\Downloads\geckodriver\geckodriver.exe", # Need path to selenium's webdriver (firefox/chrome)
    "chaptersizefactor"     :2,          # Integer value 1 or more, Denominator for splitting the chapter into multiple parts (default: 1, translate full chapter)
    "ChangeVoiceToMale"     :1,          # Optional, 0 to not change, 1 to change
    "translateNextChapter"  :0,          # Optional, 0 to not read next chapter. Input n where n > 0 and n is an integer, to read n chapters
}

# Access Data/Content from these URL
class Parse:
    def __init__(self, link):                                               # Initialize .html .data .nextpage
        self.html = self.request(self, link).text                           # Shows html source as text
        self.data = self.SoupParseContent(self, self.request(self, link))   # Shows the whole content/story text (string)
        self.nextpage = self.nexturl(self, self.request(self, link))        # Shows the URL to the next page/chapter
        self.splitdata = self.splitter(self, self.data, paramDict['chaptersizefactor']) # Shows story text (string) in a list

    @staticmethod
    def request(self, link):
        resp = requests.get(link)                                      # Access website with get request
        resp.raise_for_status()                                        # Check if get request worked/downloaded
        txt = resp.text                                                # Convert html code to text
        soup = BeautifulSoup(txt, "lxml")                              # Convert html text to soup object
        return soup

    @staticmethod
    def SoupParseContent(self, soupobj): #*** Need to modify parsing depending on website to get content/story
        # Parse Data/Content
        content = soupobj.find("div", id="contentbox")                 # Parsing the content/story in div id = contentbox
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
    def splitter(self, string, denominator):                           # String is split into multiple parts then store and return as list
        splitlength = len(string)//denominator
        return [string[x : splitlength + x] for x in range(0, len(string), splitlength)]


    @staticmethod
    def nexturl(self, soupobj):                                        # Parse link to next page/chapter and return partial url
        result = soupobj.find("a", id="next")                          # Example "/b/("some numbers").html"
        return result["href"]


# Input text to the text field on bing
def inputText(webdriverobj, translateText):
    bingTextbox = webdriverobj.find_element_by_id("t_sv")
    bingTextbox.send_keys(translateText)
    print("Input Text Completed")

# Start audio translation
def playaudio(webdriverobj):
    playButton = webdriverobj.find_element_by_id("t_srcplaycIcon")
    playButton.click()
    print("Starting To Translate Audio: ")


# Find out when translation/audio stop
def verifyAudioStop(webdriverobj):

    WebDriverWait(webdriverobj, 300).until(                                         # Wait for element to appear
        EC.presence_of_element_located((By.CSS_SELECTOR, "#t_srcplaycIcon.audio.audiofocus"))
        )
    print("Audio Start")

    WebDriverWait(webdriverobj, 1200).until(                                        # Wait for element to disappear
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "#t_srcplaycIcon.audio.audiofocus"))   # Invis is slow, try to find a faster confirming method
        )

    print("Audio Stop")

# Clear text
def cleartext(webdriverobj):
   # (browser.find_element_by_id("t_edc")).click()           # Method 1, clicking the clear button on bing's website.
    cleartextbox = webdriverobj.find_element_by_id("t_sv")   # Method 2, delete text without reloading bing translate
    cleartextbox.clear()
    print("Clear Text")

# Main Wrapper function that accepts split data for input to text
# then plays the audio, verify audio stopped, and clear text.
def inputTextPlayClear(webdriverobj, splitstring):
    # Due to the way the string is split by // (floor divide) there might be a tail with 1-2 characters
    # This if statement is for efficiency by attaching the tail element to the previous element.
    if len(splitstring) > 1 and len(splitstring[-1]) < len(splitstring[-2]) / 10:  # If the tail (last element) is less than 10% of the previous string
        splitstring[-2] += splitstring[-1]                                         # attach last element to element before last and remove last element
        splitstring.pop()

    for x in range(len(splitstring)):                     # Input, play, verify, clear over split strings
        inputText(webdriverobj, splitstring[x])
        playaudio(webdriverobj)
        verifyAudioStop(webdriverobj)
        cleartext(webdriverobj)


# Change voice to male (optional), default is female.
# Only need to be set/run once at the beginning
def changevoicegen(webdriverobj, flag):
    if flag == 1:
        (WebDriverWait(webdriverobj, 300).until(  # Wait for button to be clickable
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#t_inauoption"))  # Click Voice Drag Down Option Button
        )).click()

        (WebDriverWait(webdriverobj, 300).until(  # Wait for button to be clickable
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#t_genradio_M_0"))  # Click Male Voice radio button
        )).click()

        print("Voice Changed to Male Completed")


# __Main__
def main():

    # Below here is map out to bing translator, other translate website won't work.
    browser = webdriver.Firefox(executable_path = paramDict['webdriver'])
    browser.get("https://www.bing.com/translator")
    browser.implicitly_wait(30)                     # Global wait, will produce exception if no element is found within 30 secs

    # Webdriver Manipulation
    # Select language to Simpified Chinese (what I wanted to listen to)
    # Since it's a drop list selector with options select element will be use.

    langSelect = Select(browser.find_element_by_id("t_sl"))                  # Select drop off list
    langSelect.select_by_visible_text(paramDict['language'])                 # Selecting based on text using variable lang
    print("Language Selected: ", paramDict['language'])                      # Output current task

    inputText(browser, "Initial Set Up, changing gender voice if needed: ")

    changevoicegen(browser, paramDict['ChangeVoiceToMale'])

    cleartext(browser)

    website = Parse(paramDict['fullchapterurl'])      # Initialize Parse object of website

    inputTextPlayClear(browser, website.splitdata)    # Translate current chapter in fullchapterurl

    # Translate next chapter
    # RepeatLoop: updateweb paste start verify clear loop for next chapter (optional)
    for x in range(1, paramDict['translateNextChapter'] + 1):
        print("Next Chapter Translating: ")
        print("URL: ", paramDict['baseurl'] + website.nextpage)
        website = Parse(paramDict['baseurl'] + website.nextpage)
        inputTextPlayClear(browser, website.splitdata)


# main execute
if __name__ == "__main__":
    main()