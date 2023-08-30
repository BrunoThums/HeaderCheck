# HeaderCheck
A tool to checking headers that reveal information

## Install
- `wget https://raw.githubusercontent.com/BrunoThums/HeaderCheck/main/setup.sh; chmod +x setup.sh; sudo ./setup.sh`
 É possível mudar essa instalação. Baixe a ferramenta no linux/kali, dê permissão de execução para o setup.sh e faça o commit. Assim dará pra mudar para:
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
- OBS: if there's some URLs with errors, save to a file and run:
 - `hc_c file`

## What it can do?
- (Obviously) check some headers of a single URL or a file of URLs []
- Convert URL from http to https
- Add https:// to every URL (if there's none)
- Add port 80 and 443 to URL that doesn't contain a port especified (optionally)
- Get rid off for duplicates in file
- Show which URL's don't have:
  - Content-Security-Police
  - Strict-Transport-Security

### Other funcionalities
- You can run it anywhere
<!-- - Automatically check if sslscan is installed and. If not, then install -->

## Useful links and tips:
- [termcolor lib]([url](https://pypi.org/project/termcolor/))
- [ASCII Generator]([url](https://patorjk.com/software/taag/))

## TO-DO
- Remove www from URLs
- Add (more) custom message for invalid host or error
- Check for duplicates in URL report error list

## How to remove
- `sudo rm /usr/bin/hc; sudo rm /usr/bin/hc_h`


