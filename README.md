# HobbyWebScraping

<p>Hi, I enjoy listening to lightnovel stories, but I'm tired of copy and pasting words into a translator and clicking audio.
Which led to this script made by using Python to automate the process. This a proof of concept example and for personal use. Feel free to modify it and fit to your own needs if anything here inspires you.</p>

<ol>
<li>The script is made to scape data from https://www.uukanshu.com (where I read light novel chapters). </li> 
<li>Parse and convert the data into readable text.                                                      </li> 
<li>Open Firefox browser (can be other browsers such as chrome).                                        </li> 
<li>Uses Bing translator to convert it to audio.                                                        </li> 
</ol>

<h2> SETUP: </h2>
<p>The script requires the following python packages to work (I recommend you to install in python venv).</p>

<h3>requests install:</h3> 

>pip install requests

<h3>beautifulsoup4 install:</h3>

>pip install beatifulsoup4

<h3>selenium install:</h3>

>pip install selenium

<h3>Final Step:</h3>

<p> To run Selenium you will need geckodriver.exe for firefox, or chrome's driver for chrome. </p>

> browser = webdriver.Firefox(executable_path = r'(PUT PATH TO DRIVER HERE)') 

<h4>Extra info:</h4>
  
<p> The method SoupParseContent() needs to be changed in order to parse correct story text depending on the website in the url.

Beatifulsoup supports external parsers like lxml and htmllib5. They all got pros and cons chose them wisely if you want to optimize your program.

Selenium is a really powerful and useful library for automating tasks on browser, it was pretty fun to learn and use.
<p>
