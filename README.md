# Password Manager (CLI)                                                                            
                                                                                                      
  ## Sobre                                                                                            
  Gerenciador de senhas local escrito em Python com criptografia AES-256 e autenticação por senha     
  mestra.                                                                                             
                                                                                                      
  ## Funcionalidades
  - Criptografia AES-256                                                                              
  - Interface via terminal
  - Armazenamento em ~/password-manager/.pw_manager                                                   
                                                                                                      
  ## Instalação                                                                                       
  ```bash                                                                                             
  pip install cryptography                                                                            
                                                                                                      
  Uso                                                                                                 
                                                                                                      
  python cli.py add github.com meu_usuario                                                            
  python cli.py get github.com                                                                        
  python cli.py rm gitlab.com                                                                         
  EOL                                                                                                 
                                                                                                      
  4. **Commit da documentação:**                                                                      
  ```bash                                                                                             
  git add README.md                                                                                   
  git commit -m "Add initial documentation"                                                           
  git push origin main
