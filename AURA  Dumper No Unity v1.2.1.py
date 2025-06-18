#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
#  AURA  Dumper No Unity v1.2.1
#  Uma ferramenta de dump de alta performance para Radare2.
#  Conceito e Desenvolvimento por: Seu Assistente Gemini
#  Interface AURA e Inspiração: kirafp55
# =============================================================================

# =============================================================================
#  1. IMPORTS E DEPENDÊNCIAS
# =============================================================================
import os
import sys
import shutil
import re
from datetime import datetime
import time
import math
import zipfile
import tempfile

def check_dependencies():
    """Verifica se os módulos necessários estão instalados e guia o usuário."""
    try:
        from colorama import init, Fore, Style; import r2pipe; from tqdm import tqdm
    except ImportError as e:
        module_name = e.name; print(f"\n[✗] ERRO: Biblioteca Python necessária não encontrada: '{module_name}'.\n    Instale com: pip install {module_name}"); sys.exit(1)

check_dependencies()
from colorama import init, Fore, Style
import r2pipe
from tqdm import tqdm

# =============================================================================
#  2. AURA UI ENGINE
# =============================================================================
THEME = {}
def init_engine():
    global THEME; init(autoreset=True)
    cores = {"primary": "LIGHTYELLOW_EX", "secondary": "CYAN", "highlight": "GREEN", "dim": "LIGHTBLACK_EX", "success": "GREEN", "warning": "YELLOW", "error": "RED"}
    THEME = {key: getattr(Fore, value.upper(), Fore.WHITE) for key, value in cores.items()}

def strip_ansi(text): return re.sub(r'\x1b\[[0-9;]*[mK]', '', text)
def center_ansi(text, width): return (' ' * max(0, (width - len(strip_ansi(text))) // 2)) + text
def clear_screen(): os.system('cls' if os.name == 'nt' else 'clear')

def draw_banner(width):
    versao = "v1.2.1 BR"; titulo = "A U R A   NO UNITY   D U M P E R"
    subtitulo = "D U M P E R   D E   F U N Ç Õ E S   C O M   R A D A R E 2"
    creditos = f"Interface por: {THEME['highlight']}{Style.BRIGHT}kirafp55{Style.NORMAL}{THEME['dim']}"
    clear_screen(); print(f"\n{THEME['dim']}╔{'═' * (width - 2)}╗")
    print(f"║{center_ansi(f'{THEME["primary"]}{Style.BRIGHT}{titulo}{Style.RESET_ALL}', width - 2)}              ║")
    print(f"║{center_ansi(f'{THEME["secondary"]}{subtitulo}{Style.RESET_ALL}', width - 2)} ║")
    print(f"╟{'─' * (width - 2)}╢"); print(f"║{center_ansi(f'{THEME["success"]}{Style.BRIGHT}{versao}{Style.RESET_ALL}', width - 2)}                         ║")
    print(f"║{center_ansi(creditos, width - 2)}                  ║"); print(f"╚{'═' * (width - 2)}╝")
    timestamp = datetime.now().strftime("☆>>%d/%m/%Y <<💠>>%H:%M:%S<<☆")
    print(center_ansi(f"{THEME['highlight']}{timestamp}{Style.RESET_ALL}", width))

def draw_panel(width, panel_title, content_lines, footer=""):
    print(f"\n{THEME['dim']}╔{'═' * (width - 2)}╗")
    print(f"║{THEME['secondary']}{Style.BRIGHT}{panel_title.upper().center(width-2)}{THEME['dim']}║")
    print(f"╟{'─' * (width-2)}╢")
    if not content_lines: print(f"║ {THEME['warning']}{'Nenhuma informação para exibir.'.center(width-4)}{THEME['dim']} ║")
    for line in content_lines:
        padding_extra = len(line) - len(strip_ansi(line))
        print(f"║ {line:<{width-4+padding_extra}}{THEME['dim']} ║")
    if footer:
        print(f"╟{'─' * (width-2)}╢"); print(f"║{center_ansi(footer, width-2)}{THEME['dim']}║")
    print(f"╚{'═' * (width - 2)}╝")

# =============================================================================
#  3. LÓGICA DO DUMPER
# =============================================================================
def run_analysis_command(r2, command, description):
    print(f"\n{THEME['primary']}{description}...{Style.RESET_ALL}")
    start_time = time.time(); r2.cmd(command); end_time = time.time()
    print(f"{THEME['success']}[✓] Análise '{command}' concluída em {end_time - start_time:.2f} segundos."); time.sleep(1.5)

def analysis_options_menu(r2, width):
    while True:
        draw_banner(width); menu_title = "PASSO 2: ESCOLHA O NÍVEL DE ANÁLISE"
        menu_options = [f"{THEME['highlight']}1{Style.RESET_ALL} - {THEME['success']}Análise Rápida (aa){Style.RESET_ALL}   - Rápida, baixo uso de memória.", f"{THEME['highlight']}2{Style.RESET_ALL} - {THEME['warning']}Análise Padrão (aap){Style.RESET_ALL}  - Analisa referências, normal.", f"{THEME['highlight']}3{Style.RESET_ALL} - {THEME['error']}Análise Profunda (aaa){Style.RESET_ALL} - Completa, mas PODE TRAVAR.", "", f"{THEME['highlight']}0{Style.RESET_ALL} - Cancelar"]
        draw_panel(width, menu_title, menu_options)
        choice = input(f"\n{THEME['highlight']}Escolha uma opção: {Style.RESET_ALL}").strip()
        if choice == '1': run_analysis_command(r2, 'aa', 'Executando Análise Rápida'); return True
        elif choice == '2': run_analysis_command(r2, 'aap', 'Executando Análise Padrão'); return True
        elif choice == '3':
            confirm = input(f"\n{THEME['error']}{Style.BRIGHT}[!!] AVISO: A Análise Profunda pode consumir MUITA RAM e travar.\n    Tem certeza que deseja continuar? (s/n): {Style.RESET_ALL}").lower()
            if confirm == 's': run_analysis_command(r2, 'aaa', 'Executando Análise Profunda'); return True
            return False
        elif choice == '0': return False
        else: print(f"\n{THEME['error']}[✗] Opção inválida."); time.sleep(1)

def dump_all_functions(r2, output_file, dump_command):
    functions = r2.cmdj('aflj')
    if not functions: return False, 0
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"// Dump gerado pelo AURA  Dumper No unity v1.2.1\n")
        f.write(f"// Arquivo: {os.path.basename(r2.cmdj('ij')['core']['file'])}\n")
        f.write(f"// Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"// Total de Funções: {len(functions)}\n\n")
        with tqdm(total=len(functions), desc=f"{THEME['secondary']}Dumping de Funções{Style.RESET_ALL}", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
            for func in functions:
                # --- CORREÇÃO DE LÓGICA AQUI ---
                # 1. Primeiro, definimos o offset.
                offset = func.get('offset')
                if offset is None: continue # Pula se a função não tiver offset
                
                # 2. Depois, usamos o offset para criar um nome padrão se necessário.
                name = func.get('name', f"fcn_{offset:x}")
                
                r2.cmd(f"s {offset}")
                decompiled_code = r2.cmd(dump_command)
                
                f.write(f"// ==================================================\n")
                f.write(f"// Função: {name} @ 0x{offset:08x}\n")
                f.write(f"// ==================================================\n")
                f.write(decompiled_code + "\n\n"); pbar.update(1)
    return True, len(functions)

def select_file_from_path(width):
    current_dir = os.getcwd()
    while True:
        draw_banner(width)
        path = input(f"\n{THEME['highlight']}Digite o caminho para o arquivo .so (ou pasta): {Style.RESET_ALL}").strip().strip("'\"")
        if not path: path = current_dir
        if not os.path.exists(path): print(f"\n{THEME['error']}[✗] Caminho não encontrado."); time.sleep(2); continue
        if os.path.isfile(path):
            if path.lower().endswith(('.so', '.elf')): return path
            else: print(f"\n{THEME['error']}[✗] O arquivo não parece ser um binário compatível."); time.sleep(2); continue
        if os.path.isdir(path):
            current_dir = os.path.abspath(path)
            files = [f for f in os.listdir(path) if f.lower().endswith(('.so', '.elf')) and not f.startswith('.')]
            if not files: print(f"\n{THEME['warning']}[!] Nenhum arquivo .so ou .elf encontrado na pasta."); time.sleep(2); continue
            draw_banner(width); print(f"\n{center_ansi('SELECIONE UM ARQUIVO PARA ANALISAR', width)}")
            for i, f in enumerate(files, 1): print(center_ansi(f"{THEME['highlight']}{i}{Style.RESET_ALL} - {f}", width))
            try:
                choice_str = input(f"\n{THEME['highlight']}Escolha um arquivo (ou 0 para digitar outro caminho): {Style.RESET_ALL}")
                if not choice_str: continue
                choice = int(choice_str)
                if choice == 0: continue
                if 1 <= choice <= len(files): return os.path.join(path, files[choice - 1])
            except (ValueError, IndexError): print(f"\n{THEME['error']}[✗] Escolha inválida."); time.sleep(1.5)

# =============================================================================
#  4. FUNÇÃO PRINCIPAL (MAIN)
# =============================================================================
def main():
    init_engine()
    while True:
        try: width = os.get_terminal_size().columns
        except OSError: width = 80
        
        r2 = None
        draw_banner(width)
        caminho_do_arquivo = select_file_from_path(width)
        if not caminho_do_arquivo: break
        
        try:
            print(f"\n{THEME['primary']}Abrindo o arquivo com Radare2...{Style.RESET_ALL}")
            r2 = r2pipe.open(caminho_do_arquivo)
            print(f"{THEME['success']}[✓] Arquivo aberto.")
            time.sleep(1)

            if not analysis_options_menu(r2, width):
                if r2: r2.quit(); continue
            
            draw_banner(width)
            draw_panel(width, "PASSO 3: ESCOLHA O FORMATO DO DUMP", [
                f"{THEME['highlight']}1{Style.RESET_ALL} - Assembly Raw ({THEME['secondary']}pds{Style.RESET_ALL}) - Padrão, focado no símbolo.",
                f"{THEME['highlight']}2{Style.RESET_ALL} - Decompilação C ({THEME['secondary']}pdr{Style.RESET_ALL}) - Mais legível, pode falhar.",
                f"{THEME['highlight']}3{Style.RESET_ALL} - Assembly arm ({THEME['secondary']}pd5{Style.RESET_ALL}) - Formato alternativo."])
            dump_choice = input(f"\n{THEME['highlight']}Qual formato de dump você deseja? (1/2/3): {Style.RESET_ALL}").strip()
            
            dump_cmd, file_ext = "", ""
            if dump_choice == '1': dump_cmd, file_ext = "pds", "Raw.cs"
            elif dump_choice == '2': dump_cmd, file_ext = "pdr", "C#.cs"
            elif dump_choice == '3': dump_cmd, file_ext = "pd5", "ARM.cs"
            else: print(f"\n{THEME['error']}[✗] Opção inválida."); time.sleep(2); continue

            input_directory = os.path.dirname(caminho_do_arquivo)
            base_name = os.path.splitext(os.path.basename(caminho_do_arquivo))[0]
            output_filename = f"{base_name}_{file_ext}"
            full_output_path = os.path.join(input_directory, output_filename)

            success, count = dump_all_functions(r2, full_output_path, dump_cmd)
            
            clear_screen(); draw_banner(width)
            if success:
                draw_panel(width, "PROCESSO CONCLUÍDO", [f"{THEME['success']}{count} funções foram salvas com sucesso!", f"Arquivo de saída:", f"{THEME['highlight']}{os.path.abspath(full_output_path)}"])
            else:
                draw_panel(width, "ERRO", ["Nenhuma função foi encontrada para dumpar."])
                
        except Exception as e:
            print(f"\n{THEME['error']}[✗] Um erro fatal ocorreu: {e}")
        finally:
            if r2: r2.quit()

        if input(f"\n{THEME['highlight']}Deseja analisar outro arquivo? (s/n): {Style.RESET_ALL}").lower() != 's': break

    print(f"\n{THEME['primary']}Obrigado por usar o AURA  Dumper No Unity!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()