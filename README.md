# docToDocx-server
A flask server that converts .doc documents to .docx files using LibreOffice


## How to use
1. The server runs on port 5001.
2. Create a config file using the desription below.
3. Create a diretory called "uploads" in the same folder
4. To use the server, just send a Multipart form with the field 'file' and your file as the value to the server. You then get the converted file a few seconds later as a response.



## Config
**It is necessary to have a config file**. 
The config file should look like this:

```ini
[config]
libreoffice_bin = soffice
allow_origins = http://localhost:8080,https://realmayus.xyz
```

**allow_origins**: The origins that should get the Access-Control-Allow-Origin header (which is necessary for browsers to carry out the request)

**libreoffice_bin**: A libreoffice executable. If you install it using apt-get on Ubuntu, LibreOffice should be in your PATH as "soffice". If you're using macOS, the binary can be found at `/Applications/LibreOffice.app/Contents/MacOS/soffice`
