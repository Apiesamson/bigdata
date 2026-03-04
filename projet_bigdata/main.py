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
    """Exécute un script et affiche le résultat"""
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
            print(f"✅ {script_name} exécuté avec succès")
            print(f"⏱️  Temps d'exécution : {time.time() - start_time:.2f} secondes")
            if result.stdout:
                print("\n📋 Résultats principaux :")
                lines = result.stdout.strip().split('\n')
                for line in lines[-5:]:  # Affiche les 5 dernières lignes
                    print(f"   {line}")
        else:
            print(f"❌ Erreur lors de l'exécution de {script_name}")
            print(f"Code d'erreur : {result.returncode}")
            if result.stderr:
                print(f"Message d'erreur : {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout lors de l'exécution de {script_name}")
        return False
    except Exception as e:
        print(f"💥 Exception : {e}")
        return False
    
    return True

def check_files():
    """Vérifie que les fichiers nécessaires existent"""
    required_files = [
        "GlobalLandTemperaturesByMajorCity.csv",
        "step1_analysis_optimized.py",
        "step2_reduction_optimized.py", 
        "step3_target_creation_optimized.py",
        "step4_prepare_sipina_optimized.py",
        "step5_analysis_sipina_optimized.py"
    ]
    
    print("🔍 Vérification des fichiers requis...")
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
            print(f"❌ {file}")
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"\n⚠️  Fichiers manquants : {missing_files}")
        return False
    
    print("✅ Tous les fichiers requis sont présents")
    return True

def show_summary():
    """Affiche le résumé final"""
    print(f"\n{'='*80}")
    print("🎉 RÉSUMÉ FINAL DE L'EXÉCUTION")
    print(f"{'='*80}")
    
    # Vérification des fichiers générés
    output_files = [
        "dataset_reduced.csv",
        "dataset_with_target.csv", 
        "dataset_final_sipina.csv"
    ]
    
    print("\n📊 Fichiers de données générés :")
    for file in output_files:
        if Path(file).exists():
            size = Path(file).stat().st_size / 1024  # KB
            print(f"✅ {file} ({size:.1f} KB)")
        else:
            print(f"❌ {file}")
    
    # Vérification des visualisations
    output_dir = Path("outputs")
    if output_dir.exists():
        png_files = list(output_dir.glob("*.png"))
        txt_files = list(output_dir.glob("*.txt"))
        print(f"\n📈 Visualisations générées :")
        print(f"   🖼️  Images PNG : {len(png_files)}")
        print(f"   📝 Fichiers TXT : {len(txt_files)}")
    else:
        print("\n❌ Dossier 'outputs' non trouvé")
    
    print(f"\n📚 Prochaines étapes :")
    print(f"   1. Consultez les visualisations dans le dossier 'outputs/'")
    print(f"   2. Compilez le rapport LaTeX : compile_rapport.bat")
    print(f"   3. Importez 'dataset_final_sipina.csv' dans Sipina")
    
    print(f"\n✨ Projet terminé avec succès !")

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DU PROJET D'ANALYSE CLIMATIQUE")
    print(f"{'='*80}")
    
    # Vérification préliminaire
    if not check_files():
        print("\n❌ Vérification échouée. Arrêt du programme.")
        return
    
    # Création du dossier outputs
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    print(f"📁 Dossier 'outputs' prêt")
    
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
            print(f"⚠️  Échec de l'étape : {description}")
            continue
        
        input("\n⏸️  Appuyez sur Entrée pour continuer à l'étape suivante...")
    
    # Résumé final
    if failed_steps:
        print(f"\n❌ Étapes échouées : {failed_steps}")
    else:
        show_summary()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Exécution interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n💥 Erreur inattendue : {e}")
    finally:
        print(f"\n{'='*80}")
        print("Fin du programme")
        print(f"{'='*80}")
