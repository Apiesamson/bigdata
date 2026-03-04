"""
Script principal pour exécuter toutes les étapes du projet d'analyse climatique
Auteur: Master 2 Big Data
Date: Mars 2026
"""

import subprocess
import sys
import time
from pathlib import Path

def run_script(script_name, description):
    """Exécute un script Python via l'interpréteur courant.

    Args:
        script_name: Nom (ou chemin relatif) du script à exécuter.
        description: Libellé lisible affiché dans la console.

    Returns:
        True si le script termine avec un code retour 0, sinon False.
    """
    print(f"\n{'='*80}")
    print(f"ÉTAPE : {description}")
    print(f"Script : {script_name}")
    print(f"{'='*80}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, script_name], 
            capture_output=True, 
            text=True, 
            timeout=180
        )
        
        if result.returncode == 0:
            print(f"[OK] {script_name} exécuté avec succès")
            print(f"Temps d'exécution : {time.time() - start_time:.2f} secondes")
            if result.stdout:
                print("\nRésultats principaux :")
                lines = result.stdout.strip().split('\n')
                for line in lines[-5:]:  # Affiche les 5 dernières lignes
                    print(f"   {line}")
        else:
            print(f"[ERREUR] Erreur lors de l'exécution de {script_name}")
            print(f"Code d'erreur : {result.returncode}")
            if result.stderr:
                print(f"Message d'erreur : {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"[ERREUR] Timeout lors de l'exécution de {script_name}")
        return False
    except Exception as e:
        print(f"[ERREUR] Exception : {e}")
        return False
    
    return True

def check_files():
    """Vérifie la présence des fichiers indispensables au pipeline."""
    required_files = [
        "GlobalLandTemperaturesByMajorCity.csv",
        "step1_analysis_optimized.py",
        "step2_reduction_optimized.py", 
        "step3_target_creation_optimized.py",
        "step4_prepare_sipina_optimized.py",
        "step5_analysis_sipina_optimized.py"
    ]
    
    print("Vérification des fichiers requis...")
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
            print(f"[MANQUANT] {file}")
        else:
            print(f"[OK] {file}")
    
    if missing_files:
        print(f"\n[ERREUR] Fichiers manquants : {missing_files}")
        return False
    
    print("Tous les fichiers requis sont présents")
    return True

def show_summary():
    """Affiche un résumé des artefacts générés par le pipeline."""
    print(f"\n{'='*80}")
    print("RÉSUMÉ FINAL DE L'EXÉCUTION")
    print(f"{'='*80}")
    
    # Vérification des fichiers générés
    output_files = [
        "dataset_reduced.csv",
        "dataset_with_target.csv", 
        "dataset_final_sipina.csv"
    ]
    
    print("\nFichiers de données générés :")
    for file in output_files:
        if Path(file).exists():
            size = Path(file).stat().st_size / 1024  # KB
            print(f"{file} ({size:.1f} KB)")
        else:
            print(f"[MANQUANT] {file}")
    
    # Vérification des visualisations
    output_dir = Path("outputs")
    if output_dir.exists():
        png_files = list(output_dir.glob("*.png"))
        txt_files = list(output_dir.glob("*.txt"))
        print(f"\nVisualisations générées :")
        print(f"   Images PNG : {len(png_files)}")
        print(f"   Fichiers TXT : {len(txt_files)}")
    else:
        print("\n[MANQUANT] Dossier 'outputs' non trouvé")
    
    print(f"\nProchaines étapes :")
    print(f"   1. Consultez les visualisations dans le dossier 'outputs/'")
    print(f"   2. Compilez le rapport LaTeX : compile_rapport.bat")
    print(f"   3. Importez 'dataset_final_sipina.csv' dans Sipina")
    
    print(f"\nProjet terminé.")

def main():
    """Point d'entrée principal.

    - Vérifie les prérequis (fichiers)
    - Crée le dossier outputs
    - Exécute les scripts d'étapes (versions optimisées)
    - Affiche un résumé final
    """
    print("DÉMARRAGE DU PROJET D'ANALYSE CLIMATIQUE")
    print(f"{'='*80}")
    
    # Vérification préliminaire
    if not check_files():
        print("\n[ERREUR] Vérification échouée. Arrêt du programme.")
        return
    
    # Création du dossier outputs
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    print("Dossier 'outputs' prêt")
    
    # Liste des étapes à exécuter
    steps = [
        ("step1_analysis_optimized.py", "Analyse exploratoire des données"),
        ("step2_reduction_optimized.py", "Réduction du volume de données"),
        ("step3_target_creation_optimized.py", "Création de la variable cible"),
        ("step4_prepare_sipina_optimized.py", "Préparation des données pour Sipina"),
        ("step5_analysis_sipina_optimized.py", "Modélisation avec arbre de décision")
    ]
    
    # Exécution des étapes
    failed_steps = []
    for script, description in steps:
        if not run_script(script, description):
            failed_steps.append(script)
            print(f"[ERREUR] Échec de l'étape : {description}")
            continue
        
        input("\nAppuyez sur Entrée pour continuer à l'étape suivante...")
    
    # Résumé final
    if failed_steps:
        print(f"\n[ERREUR] Étapes échouées : {failed_steps}")
    else:
        show_summary()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExécution interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n[ERREUR] Erreur inattendue : {e}")
    finally:
        print(f"\n{'='*80}")
        print("Fin du programme")
        print(f"{'='*80}")
