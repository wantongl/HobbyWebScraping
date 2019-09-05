import requests                                                        # Accessing website pages
from bs4 import BeautifulSoup                                          # Use for parsing
from selenium import webdriver                                         # Use for running browser (firefox)
from selenium.webdriver.support.ui import Select                       # For drop down list selections
from selenium.webdriver.common.by import By                            # -|
from selenium.webdriver.support.ui import WebDriverWait                # Use for verifying translation is done
from selenium.webdriver.support import expected_conditions as EC       # -|

# Parameters
KARGS ={
    "CHAPTERURL"            :"https://www.uukanshu.com/b/71643/13068.html",
    "BASEURL"               :"https://www.uukanshu.com",
    "TRANSLATORURL"         :"https://www.bing.com/translator",
    "LANGUAGE"              :"Chinese Simplified",
    "WEBDRIVERPATH"         :r"{PUT PATH TO DRIVER HERE}\geckodriver.exe", # Path to selenium's webdriver (firefox/chrome)
    "CHAPTERSIZEFACTOR"     :2,          # Integer value 1 or more, Denominator for splitting the chapter into multiple parts (default: 1, translate  chapter)
    "CHANGEVOICETOMALE"     :0,          # Optional, 0 to not change, 1 to change
    "TRANSLATENEXTCHAPTER"  :0,          # Optional, 0 to not read next chapter. Input n where n > 0 and n is an integer, to read n chapters
}

# Access Data/Content from these URL
class Parse:
    def __init__(self, link):                                               # Initialize .html .data .nextpage
        self.html = self.request(self, link).text                           # Shows html source as text
        self.data = self.SoupParseContent(self, self.request(self, link))   # Shows the whole content/story text (string)
        self.nextpage = self.nexturl(self, self.request(self, link))        # Shows the URL to the next page/chapter
        self.splitdata = self.splitter(self, self.data, KARGS['CHAPTERSIZEFACTOR']) # Shows story text (string) in a list

    @staticmethod
    def request(self, link):
        resp = requests.get(link)                                      # Access website with get request
        resp.raise_for_status()                                        # Check if get request worked/downloaded
        txt = resp.text                                                # Convert html code to text
        soup = BeautifulSoup(txt, "html.parser")                       # Convert html text to soup object
                                                                       # Other external parsers are available(lxml and htmllib5)
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


class Browser:

    def __init__(self):
        # initializer and instance attributes
        self.webdriverobj = webdriver.Firefox(executable_path = KARGS['WEBDRIVERPATH'])
        self.novel_parse = Parse(KARGS['CHAPTERURL'])  # Initialize Parse object of website

        self.webdriverobj.get(KARGS['TRANSLATORURL'])

    def wait(self, secs):
        # Global wait, will produce exception if no element is found within 30 secs
        self.webdriverobj.implicitly_wait(30)

    def change_language(self, element_id_of_language_select = "tta_srcsl"):
        lang_selector = Select(self.webdriverobj.find_element_by_id(element_id_of_language_select))    # Select drop off list
        lang_selector.select_by_visible_text(KARGS['LANGUAGE'])                                        # Selecting based on text using variable lang
        print("Language Selected: ", KARGS['LANGUAGE'])                                                # Output current task

    def input_text(self, text, element_id_of_textarea):
        # Input text to the text field on bing
        bingTextbox = self.webdriverobj.find_element_by_id(element_id_of_textarea)
        bingTextbox.send_keys(text)
        print("Input Text Completed")


    def playaudio(self, element_id_of_playaudio):
        # Start audio translation
        playButton = self.webdriverobj.find_element_by_id(element_id_of_playaudio)
        playButton.click()
        print("Starting To Translate Audio: ")

    # old "#t_srcplaycIcon.audio.audiofocus"
    def verify_audio_stop(self, css_id):
        # Find out when translation/audio stop
        WebDriverWait(self.webdriverobj, 300).until(  # Wait for element to appear
            EC.presence_of_element_located((By.CSS_SELECTOR, css_id))
        )
        print("Audio Start")

        WebDriverWait(self.webdriverobj, 1200).until(  # Wait for element to disappear
            EC.invisibility_of_element_located((By.CSS_SELECTOR, css_id))
            # Invis is slow, try to find a faster confirming method
        )

        print("Audio Stop")


    def clear_text(self, element_of_id_textarea):
        # Clear text
        # (browser.find_element_by_id("t_edc")).click()           # Method 1, clicking the clear button on bing's website.
        clear_textbox = self.webdriverobj.find_element_by_id(element_of_id_textarea)  # Method 2, delete text without reloading bing translate
        clear_textbox.clear()
        print("Clear Text")

    
    def input_text_play_clear(self, splitstring, element_id_of_textarea="tta_input", element_id_of_playaudio="tta_playiconsrc", css_id="#tta_play_focus"):
        # Main Wrapper function that accepts split data for input to text
        # then plays the audio, verify audio stopped, and clear text.
        # Due to the way the string is split by // (floor divide) there might be a tail with 1-2 characters
        # This if statement is for efficiency by attaching the tail element to the previous element.
        if len(splitstring) > 1 and len(splitstring[-1]) < len(
                splitstring[-2]) / 10:  # If the tail (last element) is less than 10% of the previous string
            splitstring[-2] += splitstring[-1]  # attach last element to element before last and remove last element
            splitstring.pop()

        for x in range(len(splitstring)):  # Input, play, verify, clear over split strings
            self.input_text(splitstring[x],element_id_of_textarea)
            self.playaudio(element_id_of_playaudio)
            self.verify_audio_stop(css_id)
            self.clear_text(element_id_of_textarea)

""" # Depreciated because Bing don't got the option anymore.
    # Leaving function as commented in case option returns.

    def change_voice(self, flag):
        # Change voice to male (optional), default is female.
        # Only need to be set/run once at the beginning
        if flag == 1:
            (WebDriverWait(self.webdriverobj, 300).until(  # Wait for button to be clickable
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#t_inauoption"))  # Click Voice Drag Down Option Button
            )).click()

            (WebDriverWait(self.webdriverobj, 300).until(  # Wait for button to be clickable
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#t_genradio_M_0"))  # Click Male Voice radio button
            )).click()

            print("Voice Changed to Male Completed")
"""

# __Main__
def main():
    # Below here is map out to bing translator, other translate website won't work.
    browser = Browser()                  # Start Browser
    browser.wait(30)                     # Global wait, will produce exception if no element is found within 30 secs

    # Webdriver Manipulation
    # Select Language to Simpified Chinese (what I wanted to listen to)
    # Since it's a drop list selector with options select element will be use.
    browser.change_language() # arg = element id

    # Translate current chapter in ChapterURL
    browser.input_text_play_clear(browser.novel_parse.splitdata)    

    # Translate next chapter
    # RepeatLoop: updateweb paste start verify clear loop for next chapter (optional)
    for x in range(1, KARGS['TRANSLATENEXTCHAPTER'] + 1):
        print("Next Chapter Translating: ")
        print("URL: ", KARGS['BASEURL'] + browser.novel_parse.nextpage)
        browser.novel_parse = Parse(KARGS['BASEURL'] + browser.novel_parse.nextpage)
        browser.input_text_play_clear(browser.novel_parse.splitdata)

# main execute
if __name__ == "__main__":
    main()
