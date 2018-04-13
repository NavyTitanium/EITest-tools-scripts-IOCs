# IOCs

<strike>Indicators of Compromise (IOCs) updated every 30 minutes related to EITest campaigns.</strike> **The domain stat-dns.com used in EITest's DGA algorithm [has been sinkholed](https://www.proofpoint.com/us/threat-insight/post/eitest-sinkholing-oldest-infection-chain). As a result, the EITest campaign now appears to have been shutdown since 2018-03-15.**

# backend-decipher.py

Decodes data transmitted from an infected website via the EITest script to the EITest C2.

# infol_Decrypter.py

Decodes data transmitted by the victims to help.php and download.php.

# injPayloadDecrypter.py

Decodes data transmitted from the EITest C2 to the infected website (the content to be injected in the webpage).

# parsing-EITest_GET-requests.py

Process the GET requests from the EITest sinkhole server and store them in a MySQL database. Takes as input a large log file containing millions of requests, decode and process them using multiple threads.

# Malicious files

Contains differents artefact belonging to EITest.
