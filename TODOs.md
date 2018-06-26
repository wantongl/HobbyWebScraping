# TO DOs:

1. Instead of clicking the clear button for cleartext()
Maybe add in another option to clear by selecting all text content and paste rather than sendkeys()

2. Extra optional feature end program when caught up to current chapter/final page.

3. Since bing can only translate up to 5000 words.
Another feature is to detect and split current chapter into multiple parts then translate them while keeping track.

4. Problem:
Bing audio itself sometimes stop translating or freeze up, not exactly sure what's causing it.
Can be possibly caused by uncommon characters or maybe the word list is too long.
The problem is not due to this program but with bing translator itself. Sometimes deleting previously translated
words then restarting the audio translator allows bing to continue translating where it stopped.
Pending and brain storming solution:
4.1 Detect audio, keep track if audio stops before it can finish whole story. Trim story and restart audio?
4.2 Measure translator audio speed to determine how far the story been translated. Trim story and restart?
4.3 There is far less chance of audio freezing if the words are short,
    and there is far less chance of missing important story contents due to freezing if translate part is small
    3. can maybe fix 4. by splitting the story into many parts for audio translate