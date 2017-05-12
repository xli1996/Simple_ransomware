				Ransomware ReadMe
Instructions:

Our ransomware can be downloaded from github using the link below:

https://github.com/theredhood/Simple_ransomware/raw/master/malicious%20doc.docm

For testing purpose, please create a folder at “C:\” with name “test_ground” and add some files in it. 

We assume that Microsoft Word is installed on the targeted Windows 10 machine and Word Macro is enabled.

Once the Word document is opened and Macro is enabled, the malicious executable will be downloaded to the same folder and run automatically.  A window will pop up and press “enc” will encrypt common files in “C:\test_ground\” such as .doc, .pdf, .zip, etc.. Press “dec” will decrypt these files.

Implementation:

We use python3 to build this simple ransomware. With Crypto library, we use AES-256 algorithm to encrypt files. You can set emails address and use smtp protocol to send emails. For easy testing purpose, we store the temporary password locally, and create a simple GUI. Just click “enc” to encrypt files and “dec” to decrypt files. With simple modification in the original code, we could encrypt files with specific extension and make the ransomware more malicious. Since this is just for proof of concept, our code would not do any damage to the victim’s machine.

Attack Method:

The most common way for a ransomware to get installed is by email with malicious Word attachment. An attacker can use tools such as Swaks to fake sender email address or just send spam emails with tricky subject such as “Your Tax Return Form” or “Online Order Detail”. Once a user open these attachments on their Windows machine, the malicious program can be easily downloaded and executed.

Defense Suggestion:

During developing this ransomware, we have found a few ways to defend such ransomware:
Be care of every Word or other files you download, and enable Macros cautiously.
We can use honeypot method to capture such ransomware. Put some useless Word or text files in your root directory. When those files are changed weirdly, stop the process and disconnect Internet and dump the memory. It may stop the ransomware from further executing.
Rely on some anti-virus softwares. There are some anti-virus software that could stop suspicious programs from running and monitors the files downloaded.

