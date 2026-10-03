# Flux Google Merchant — mesbonbons.net

Flux produits (texte tabulé) lu par Google Merchant Center, compte MesBonBons (5383673118). Adresse du flux : `https://raw.githubusercontent.com/yvesvandamme1975-sketch/mesbonbons-merchant-feed/main/feed.tsv`.

Régénéré à 7 h et 12 h (Europe/Brussels) par une tâche planifiée Claude : `python3 refresh.py` relit les pages produits publiques de mesbonbons.net (prix TTC, disponibilité, stock, image, nom ERP, description) pour les produits de `products.json` (identifiant ERP, adresse, EAN vérifié par 2 sources, base : fichier stock enrichi Fladis du 02/10/2026). `stock-history.csv` garde chaque relevé de stock ; `status.json` résume le dernier passage. Si moins de 80 % des produits passent, le flux précédent est conservé.

Données uniquement publiques (déjà visibles sur le site). Mise en place par Aives Consulting le 2026-10-03.
