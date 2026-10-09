# Flux Google Merchant — mesbonbons.net

Flux produits (texte tabulé) lu par Google Merchant Center, compte MesBonBons (5383673118). Adresse du flux : `https://raw.githubusercontent.com/yvesvandamme1975-sketch/mesbonbons-merchant-feed/main/feed.tsv`.

Régénéré à 7 h et 12 h (Europe/Brussels) par une tâche planifiée Claude : `python3 refresh.py` relit les pages produits publiques de mesbonbons.net (prix TTC, disponibilité, stock, image, nom ERP, description) pour les produits de `products.json` (identifiant ERP, adresse, EAN vérifié par 2 sources, base : fichier stock enrichi Fladis du 02/10/2026). `stock-history.csv` garde chaque relevé de stock ; `status.json` résume le dernier passage. Si moins de 80 % des produits passent, le flux précédent est conservé.

Données uniquement publiques (déjà visibles sur le site). Mise en place par Aives Consulting le 2026-10-03.

## Élargissement du 09/10/2026 et flux Bing / Meta

`products.json` passe de 1 900 à 3 358 produits (accord d’Yves du 09/10) : ajout des produits PRET_CATALOGUE de Fladis ayant une page mesbonbons.net, quel que soit leur stock (la disponibilité suit le stock relevé). 139 candidats dont le code-barres est partagé avec un autre produit ont été écartés (code-barres à corriger dans l’ERP avant tout ajout). Les produits sans prix ou sans description sur la page restent exclus à chaque relevé par `refresh.py`.

`feed_bing_meta.py feed.tsv stock-history.csv allowlist.json feed-bing-meta.tsv` construit le flux Bing / Meta (même format Google) à partir du flux Merchant et de la liste validée `allowlist.json` (3 404 identifiants), disponibilité selon le dernier relevé de stock. Ce fichier n’est déclaré ni dans Bing Merchant Center ni dans Meta Commerce Manager tant qu’Yves ne l’a pas décidé.

Dépôt passé en privé le 09/10/2026 à la demande d’Yves : l’adresse raw.githubusercontent.com du flux ne répond plus sans jeton ; Google Merchant Center doit être pointé vers une autre adresse publique.

