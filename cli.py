#cli.py
import argparse
import getpass
import sys
from manager.storage import (
      open_vault,
      add_entry,
      remove_entry,
      get_entry,
      persist,
  )

def main():
      parser = argparse.ArgumentParser(
          description="Gerenciador de Senhas simples (AES‑256, CLI)."
      )
      sub = parser.add_subparsers(dest="cmd", required=True)

      # add
      p_add = sub.add_parser("add", help="Adicionar ou atualizar senha")
      p_add.add_argument("site", help="Identificador do site ou serviço")
      p_add.add_argument("username", help="Nome de usuário")
      p_add.add_argument("-p", "--password", help="Senha (se omitida, será solicitada)")

      # get
      p_get = sub.add_parser("get", help="Mostrar senha salva")
      p_get.add_argument("site", help="Identificador do site")

      # rm
      p_rm = sub.add_parser("rm", help="Remover entrada")
      p_rm.add_argument("site", help="Identificador do site")

      args = parser.parse_args()

      master = getpass.getpass("Senha mestra: ")
      try:
          vault = open_vault(master)
      except ValueError:
          print("⚠  Senha mestra incorreta.", file=sys.stderr)
          sys.exit(1)

      if args.cmd == "add":
          pwd = args.password or getpass.getpass("Senha a ser salva: ")
          vault = add_entry(vault, args.site, args.username, pwd)
          persist(vault, master)
          print(f"  Entrada '{args.site}' salva/atualizada.")
      elif args.cmd == "get":
          entry = get_entry(vault, args.site)
          if not entry:
              print(f"  Entrada '{args.site}' não encontrada.")
          else:
              print(f"Site: {args.site}")
              print(f"Usuário: {entry['username']}")
              print(f"Senha: {entry['password']}")
      elif args.cmd == "rm":
          if args.site not in vault:
              print(f"  Entrada '{args.site}' inexistente.")
          else:
              vault = remove_entry(vault, args.site)
              persist(vault, master)
              print(f"  Entrada '{args.site}' removida.")
      else:
          parser.print_help()


if __name__ == "__main__":
      main()

