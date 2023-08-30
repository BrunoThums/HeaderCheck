# HeaderCheck
A tool to checking headers that reveal information

## Install
- `wget https://raw.githubusercontent.com/BrunoThums/HeaderCheck/main/setup.sh; chmod +x setup.sh; sudo ./setup.sh`
<!-- É possível mudar essa instalação. Baixe a ferramenta no linux/kali, dê permissão de execução para o setup.sh e faça o commit. Assim dará pra mudar para:
git clone https://github.com/BrunoThums/SSLVerifier.git; sudo SSLVerifier/setup.sh 
Só precisa ajustar o "local" do script, dentro dele. Porque senão ele não consegue se apagar
-->
## How to use
- You can pass a URL or a file with URLs without any treatment:
  - No need to pass http:// or https://
  - ~~No need to pass www~~ (coming soon)
  - No port required
  - Don't worry about duplicates
  - Don't worry about directories
- hc file_with_urls
- hc single_URL
- OBS: if there's some URLs with errors, save to a file and run the auxiliary script:
  - `hc_h file` (the extra data or status code come from redirects, stay aware)

## What it can do?
- (Obviously) check some headers of a single URL or a file of URLs []
- Convert URL from http to https
- Add https:// to every URL (if there's none)
- Add port 80 and 443 to URL that doesn't contain a port especified (optionally)
- Get rid off for duplicates in file
- Show which URL's don't have:
  - Content-Security-Police
  - Strict-Transport-Security

## Parameters
- `--all-headers` or `-h` -> show all headers (yep, like a normal response header)
- `--no-ports` or `-np` -> don't add ports 80 and 443, let it handle automatically
- `--no-csp-hsts` or `-nr` -> don't verify CSP or HSTS
- `--debug` or `-d` -> show detailed errors
- `--show-instant-errors` or `-si` -> show, at the instant, connection errors
- All parameters are **False** by default

## Notes
- As it is an automated software, there may be inconsistencies. It is interesting to print the headers directly in the browser. The tool is just for automating the process of finding specific headers (or lack thereof)

## Useful links and tips:
- [termcolor lib](https://pypi.org/project/termcolor/)
- [ASCII Generator](https://patorjk.com/software/taag/) (this theme: slant)
- How to print an ASCII image?
  - (bash) Save in a txt, type `cat image.txt | gzip | base64` in terminal, copy and paste into script `base64 -d <<<"yourBase64image" | gunzip` (that's it, only ctrl+v, don't add new lines or remove new lines, leaves as it is)
  - (python) Add a bunch of print's for each line

## TO-DO
- Remove www from URLs
- Add (more) custom message for invalid host or error
- Check for duplicates in URL report error list

## Uninstall
- `sudo rm /usr/bin/hc; sudo rm /usr/bin/hc_h`


