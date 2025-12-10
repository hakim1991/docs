# 📚 PostgreSQL - Documentation Complète

## Table des matières

### 🚀 Bases
1. [Introduction et Installation](./infos-postgresql-01-introduction-installation.md)
   - Qu'est-ce que PostgreSQL ?
   - Installation Linux / Windows
   - Première configuration
   - Commandes de base

2. [Configuration](./infos-postgresql-02-configuration.md)
   - Fichiers de configuration
   - postgresql.conf
   - pg_hba.conf
   - Memory tuning

### 💾 Gestion des données
3. [Bases de données et schémas](./infos-postgresql-03-databases-schemas.md)
   - Créer et gérer des databases
   - Schémas
   - Tables
   - Contraintes

4. [Utilisateurs et permissions](./infos-postgresql-04-users-permissions.md)
   - Rôles et users
   - GRANT et REVOKE
   - Security best practices

5. [Requêtes SQL](./infos-postgresql-05-requetes-sql.md)
   - SELECT, INSERT, UPDATE, DELETE
   - JOINs
   - Sous-requêtes
   - Fonctions et agrégats
   - CTEs et Window functions

### ⚡ Performance
6. [Index et optimisation](./infos-postgresql-06-index-optimisation.md)
   - Types d'index
   - Création d'index
   - EXPLAIN et ANALYZE
   - Query optimization
   - Vacuum et maintenance

7. [Performances avancées](./infos-postgresql-07-performances-avancees.md)
   - Connection pooling
   - Partitionnement
   - Réglages mémoire
   - Autovacuum tuning

### 🔄 Haute disponibilité
8. [Backup et restauration](./infos-postgresql-08-backup-restore.md)
   - pg_dump et pg_restore
   - Point-in-time recovery
   - Continuous archiving
   - Backup automation

9. [Réplication](./infos-postgresql-09-replication.md)
   - Streaming replication
   - Logical replication
   - Hot standby
   - Failover

### 🔧 Administration
10. [Monitoring](./infos-postgresql-10-monitoring.md)
    - pg_stat_* views
    - Performance monitoring
    - Log analysis
    - Outils de monitoring

11. [Maintenance](./infos-postgresql-11-maintenance.md)
    - Vacuum
    - Analyze
    - Reindex
    - Bloat management

12. [Troubleshooting](./infos-postgresql-12-troubleshooting.md)
    - Problèmes courants
    - Locks et deadlocks
    - Connection issues
    - Performance problems

---

## 🎯 Commandes rapides

```bash
# Connexion
psql -U postgres
psql -U user -d database -h host

# Service
sudo systemctl start postgresql
sudo systemctl stop postgresql
sudo systemctl restart postgresql
sudo systemctl status postgresql

# Commandes psql
\l              # Lister les databases
\c database     # Se connecter à une database
\dt             # Lister les tables
\du             # Lister les users
\q              # Quitter

# Backup
pg_dump database > backup.sql
pg_dumpall > full-backup.sql

# Restore
psql database < backup.sql
```

## 📖 Structure de la documentation

Chaque chapitre contient:
- ✅ Explications détaillées
- ✅ Exemples SQL
- ✅ Cas d'usage pratiques
- ✅ Best practices
- ✅ Troubleshooting

---

## 🔗 Ressources

- [Documentation officielle](https://www.postgresql.org/docs/)
- [PostgreSQL Wiki](https://wiki.postgresql.org/)
- [PostgreSQL GitHub](https://github.com/postgres/postgres)

---

**Prêt à commencer ?** → [Introduction et Installation](./infos-postgresql-01-introduction-installation.md)
