# Kaléidogram

![Status](https://img.shields.io/badge/status-work%20in%20progress-orange) ![License](https://img.shields.io/badge/license-AGPL%20v3-blue)

Un QR code par plat, les allergènes affichés en un scan. Pour les restaurateurs qui veulent être en règle sans y passer leurs soirées.

[Français](#français) | [English](#english)

---

## Français

### Le problème

Depuis le règlement européen INCO 1169/2011, tout restaurateur doit informer ses clients de la présence des 14 allergènes majeurs dans chaque plat servi. En pratique, l'affichage se fait souvent sur une fiche papier plastifiée en fin de carte, rarement à jour, illisible ou oubliée au fond du menu. Un client allergique n'a alors que deux options, demander au serveur qui n'a pas toujours l'info, ou renoncer à commander.

### La solution

Kaléidogram permet au restaurateur de saisir ses plats et leurs ingrédients une seule fois, puis de générer un QR code par plat qu'il peut poser directement sur ses tables ou sa carte. Le client scanne, voit instantanément les allergènes présents, et commande en toute confiance. Côté cuisine, mettre à jour un ingrédient met à jour tous les plats qui l'utilisent, sans avoir à réimprimer quoi que ce soit.

### Fonctionnalités

Côté restaurateur
- Gestion de la carte (plats, ingrédients, allergènes) via une interface simple
- Génération automatique d'un QR code par plat, imprimable ou intégrable à la carte
- Mise à jour centralisée, un changement d'ingrédient se propage à tous les plats concernés
- Compte protégé par mot de passe, chaque restaurant ne voit que ses propres données

Côté client final
- Scan du QR code depuis n'importe quel smartphone, sans installation
- Affichage clair des allergènes présents dans le plat
- Aucune création de compte, aucune donnée personnelle collectée

### Statut du projet

Projet en développement actif, dernière mise à jour septembre 2026.

Ce qui est fait, le backend (API, authentification, gestion complète des plats et ingrédients, protection par compte utilisateur).

Ce qui est en cours, la finalisation de la sécurisation des routes et le démarrage de l'interface web pour les restaurateurs.

Ce qui vient, la mise en test avec les premiers restaurants partenaires puis l'ouverture publique.

### Participer aux tests

Vous êtes restaurateur en Île-de-France et souhaitez tester Kaléidogram dans votre établissement, contactez-moi via GitHub (Issues du projet ou message direct sur [@theKaido](https://github.com/theKaido)).

Ce que j'attends de vous, quelques heures pour saisir votre carte, un mois d'usage réel, et vos retours honnêtes sur ce qui marche et ce qui coince.

Ce que vous obtenez, un outil gratuit, adapté à vos remarques, et une conformité INCO sans effort.

### Pourquoi ce nom ?

Un kaléidoscope génère une infinité de motifs uniques à partir d'un même principe. Kaléidogram fonctionne pareil, chaque restaurateur génère autant de QR codes qu'il a de plats, tous différents, tous liés à sa carte. Le suffixe "-gram" évoque à la fois la trace enregistrée (comme un télégramme) et la multiplicité (comme un fil Instagram).

### Licence

Kaléidogram est distribué sous licence AGPL v3. Vous pouvez l'utiliser gratuitement, l'installer chez vous, le modifier. La seule contrainte, toute modification que vous publiez ou hébergez pour d'autres doit rester ouverte et partagée. C'est un choix assumé en faveur du logiciel libre.

[LICENCE](./LICENSE)

---

## English

### The problem

Since EU regulation INCO 1169/2011, every restaurant must inform customers about the 14 major allergens present in each dish. In practice, this information usually ends up on a laminated sheet at the back of the menu, rarely up to date, hard to read, or simply forgotten. A customer with allergies then has two options, asking the waiter who often doesn't know, or giving up on ordering.

### The solution

Kaleidogram lets restaurants enter their dishes and ingredients once, then generate a QR code per dish to place on tables or menus. Customers scan, see the allergens instantly, and order with confidence. On the kitchen side, updating one ingredient updates every dish that uses it, no reprinting needed.

### Features

For restaurants
- Menu management (dishes, ingredients, allergens) through a simple interface
- Automatic QR code generation per dish, printable or embeddable in the menu
- Centralized updates, one ingredient change propagates to every relevant dish
- Password-protected accounts, each restaurant only sees its own data

For customers
- QR scan from any smartphone, no app install required
- Clear display of allergens present in the dish
- No account creation, no personal data collected

### Project status

Actively developed, last update September 2026.

Done, the backend (API, authentication, full dish and ingredient management, per-user data protection).

In progress, finalizing route protection and starting the restaurant-facing web interface.

Coming next, pilot testing with partner restaurants then public launch.

### Join the pilot

If you run a restaurant in the Paris region and want to test Kaleidogram in your venue, contact me through GitHub (project Issues or direct message on [@theKaido](https://github.com/theKaido)).

What I ask from you, a few hours to enter your menu, one month of real-world use, and honest feedback on what works and what doesn't.

What you get, a free tool, tailored to your feedback, and effortless INCO compliance.

### Why this name?

A kaleidoscope creates endless unique patterns from a single principle. Kaleidogram works the same way, each restaurant generates as many QR codes as it has dishes, all different, all tied to its menu. The "-gram" suffix hints at both the recorded trace (like a telegram) and the multiplicity (like an Instagram feed).

### License

Kaleidogram is released under the AGPL v3 license. You can use it for free, self-host it, and modify it. The only requirement, any modification you publish or host for others must remain open and shared. A deliberate choice in favor of free software.

[LICENSE](./LICENSE)

---

## Tech stack

Backend, Python 3.14, FastAPI, SQLAlchemy, PostgreSQL 18, Alembic, JWT authentication.
Frontend, React with Vite and TypeScript (in progress).
Infrastructure, Docker, GitHub Actions, Supabase (planned).

## Quick start

Requires Docker and Docker Compose.

```bash
git clone git@github.com:theKaido/kaleidogram.git
cd kaleidogram
cp .env.example .env
cp frontend/.env.example frontend/.env
docker compose up
```

The API is then available at `http://localhost:8000` (`/docs` for the interactive Swagger UI) and the frontend at `http://localhost:5173`.

For setup without Docker, running tests, linting, and coding conventions, see [CONTRIBUTING.md](./CONTRIBUTING.md).

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup, coding conventions, and how to submit pull requests.
