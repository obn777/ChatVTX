#!/bin/bash
BACKUP_DIR="/home/obn7/VTX_Backups"
mkdir -p $BACKUP_DIR
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")

# Архивируем память пользователей и базу ключей
tar -czf "$BACKUP_DIR/vtx_backup_$TIMESTAMP.tar.gz" core/personal_hub auth_data.json

echo "✅ Backup created at $BACKUP_DIR/vtx_backup_$TIMESTAMP.tar.gz"
