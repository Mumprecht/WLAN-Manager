# Manuel d’utilisation de WLAN-Manager

## Démarrage

Dans le répertoire du projet :

```powershell
python src\main.py
```

Au démarrage, Windows peut demander des droits d’administrateur.

## Afficher les profils WLAN

Après le démarrage, tous les profils WLAN enregistrés sont affichés automatiquement.

La touche `F5` permet d’actualiser la liste.

## Copier le contenu de la liste des profils

Le contenu d’une cellule du tableau peut être copié dans le presse-papiers.

Cliquez avec le bouton droit sur la cellule souhaitée et sélectionnez dans le menu contextuel :

```text
Copier    Ctrl+C
```

Vous pouvez également sélectionner la cellule souhaitée et utiliser :

```text
Ctrl+C
```

Cela permet par exemple de copier le nom du profil WLAN, l’authentification ou le contenu du mot de passe affiché dans le tableau.

## Afficher les mots de passe WLAN

Menu :

```text
WLAN > Afficher les mots de passe
```

Raccourci clavier :

```text
Ctrl+P
```

Les mots de passe sont affichés en clair.

## Se connecter à un WLAN

Un profil enregistré peut être connecté par un double-clic.

Autre possibilité :

```text
Profils > Se connecter
```

ou :

```text
Ctrl+Enter
```

## Sauvegarder les profils WLAN

Menu :

```text
Fichier > Sauvegarder les profils WLAN...
```

Il est possible de sélectionner un, plusieurs ou tous les profils.

Un nouveau sous-dossier contenant la date et l’heure peut être créé en option.

Pour ajouter des sauvegardes dans un dossier existant, désactivez cette option.

Si un fichier XML existe déjà, les options suivantes sont disponibles :

- Écraser
- Ignorer
- Annuler

## Restaurer les profils WLAN

Menu :

```text
Fichier > Restaurer les profils WLAN...
```

Il est possible de sélectionner un, plusieurs ou tous les fichiers XML.

## Supprimer les profils WLAN

Menu :

```text
Profils > Supprimer les profils WLAN...
```

Il est possible de supprimer un, plusieurs ou tous les profils.

Une demande de confirmation apparaît avant la suppression.

## Export CSV

Menu :

```text
Fichier > Exporter en CSV...
```

Le fichier CSV peut contenir des mots de passe WLAN en clair.

## Connexion WLAN actuelle

Menu :

```text
WLAN > Connexion actuelle
```

Raccourci clavier :

```text
Ctrl+I
```

## Raccourcis clavier

- `F5` Actualiser
- `Ctrl+C` Copier le contenu de la cellule sélectionnée
- `Ctrl+S` Sauvegarder
- `Ctrl+R` Restaurer
- `Suppr` Supprimer
- `Ctrl+P` Afficher les mots de passe
- `Ctrl+I` Connexion actuelle
- `Ctrl+Enter` Se connecter
- `Ctrl+Shift+S` Exporter en CSV
- `Ctrl+Q` Quitter
- `F1` À propos de WLAN-Manager

## Licence et copyright

Copyright © 2026 Urs Mumprecht / Mumprecht Software.

WLAN-Manager est un logiciel propriétaire qui peut être utilisé gratuitement à des fins privées et à d’autres fins non commerciales.

L’utilisation commerciale, la modification, la redistribution, la republication ou la création d’œuvres dérivées ne sont pas autorisées sans l’accord écrit préalable du titulaire des droits d’auteur.

La licence suivante s’applique :

**WLAN-Manager Non-Commercial License, Version 1.0**

Les conditions de licence complètes se trouvent dans le fichier `LICENSE`.

## Sécurité

Les fichiers XML de sauvegarde contenant des clés en clair ainsi que les fichiers CSV contenant des mots de passe doivent être traités de manière confidentielle.

## Code QR WLAN

Sélectionnez un profil WLAN enregistré, puis :

```text
Profils > Afficher le code QR...
```

La fonction est également disponible dans le menu contextuel du profil.

La boîte de dialogue affiche :

- SSID
- Authentification
- Mot de passe WLAN masqué
- Code QR

Le mot de passe peut être affiché si nécessaire.

Le code QR peut être enregistré au format PNG ou copié dans le presse-papiers sous forme d’image. Les smartphones et les tablettes peuvent utiliser le code pour importer les données d’accès WLAN.

Les profils WLAN Enterprise ne sont actuellement pas pris en charge.

## Aide

Avec `F1` ou via :

```text
Aide > Manuel d’utilisation
```

ce manuel d’utilisation est affiché directement dans WLAN-Manager.

Sous :

```text
Aide > Informations sur le projet
```

des informations techniques sur la version installée, Python, PySide6, Windows ainsi que le répertoire des journaux sont affichées.

Sous :

```text
Aide > À propos de WLAN-Manager
```

le nom du programme, la version, l’entreprise, le copyright et l’auteur sont affichés.

## Créer un profil WLAN

Via :

```text
Profils > Nouveau profil WLAN...
```

un nouveau profil WLAN peut être créé.

Informations requises :

- Nom du profil
- SSID
- Type de sécurité
- Mot de passe pour les WLAN sécurisés

Options supplémentaires :

- Se connecter automatiquement
- Autoriser la connexion à un SSID masqué

## Modifier un profil WLAN

Sélectionnez un profil existant et choisissez :

```text
Profils > Modifier le profil WLAN...
```

ou utilisez l’entrée correspondante du menu contextuel.

Le nom du profil, le SSID, la sécurité, le mot de passe et les options de connexion peuvent être modifiés.

### Portée et modification des profils existants

Pour un nouveau profil, il est possible de choisir :

- Tous les utilisateurs
- Utilisateur actuel uniquement

Lors de la modification d’un profil existant, WLAN-Manager reprend automatiquement sa portée actuelle. La configuration de sécurité Windows existante est également conservée. Ainsi, les profils WPA2/WPA3 plus complexes sont préservés ; pour les profils existants, l’éditeur ne modifie que le nom du profil, le SSID, le mot de passe, la connexion automatique et le paramètre relatif aux SSID masqués.

Les profils WLAN gérés par une stratégie de groupe sont en lecture seule et ne peuvent pas être modifiés.

### Mot de passe lors de la modification

Pour un nouveau WLAN sécurisé, une clé WLAN valide doit être indiquée.

Pour un profil sécurisé existant :

- Si le mot de passe existant est affiché, il peut être modifié.
- Si le champ du mot de passe est entièrement vidé, le mot de passe existant reste inchangé.
- Si Windows n’a pas pu fournir le mot de passe en clair, le champ reste vide. Dans ce cas également, un champ vide signifie : conserver le mot de passe existant.
- Ce n’est que lorsqu’un nouveau mot de passe est saisi que WLAN-Manager remplace la clé existante.

Pour les nouvelles clés WLAN Personal, WLAN-Manager accepte des phrases secrètes de 8 à 63 caractères ASCII imprimables ou un PSK hexadécimal de 64 caractères.

Aucun mot de passe n’est enregistré pour les WLAN ouverts.
