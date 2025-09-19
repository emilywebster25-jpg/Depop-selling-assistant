# 🛡️ DATA PROTECTION PROTOCOL - CRITICAL SAFETY MEASURES

## ⚠️ ABSOLUTE RULES - NEVER TO BE VIOLATED

### 1. ZERO DELETION POLICY
- **NEVER** use deletion commands (`rm`, `del`, `unlink`, etc.) on user data
- **NEVER** assume any user file is disposable or temporary
- **NEVER** delete without explicit user permission and backup confirmation

### 2. MANDATORY BACKUP PROTOCOL
Before ANY file operation that could modify or move user data:

```bash
# REQUIRED: Create timestamped backup
BACKUP_DIR="/Users/emilywebster/Dev/Depop_Selling/backups/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -R [source_files] "$BACKUP_DIR/"

# REQUIRED: Verify backup exists
ls -la "$BACKUP_DIR"

# REQUIRED: Get explicit user permission
echo "Backup created at: $BACKUP_DIR"
echo "May I proceed with [SPECIFIC_OPERATION]?"
```

### 3. SAFE OPERATIONS ONLY
- Use `mv` to move files (reversible)
- Use `cp` to duplicate files (non-destructive) 
- Create backup locations before any modifications
- Verify operations completed successfully

### 4. USER PERMISSION REQUIRED
Ask explicit permission before:
- Moving files between directories
- Modifying file contents
- Renaming files
- Any operation that changes user data location or state

### 5. VERIFICATION PROTOCOL
- Always verify backups exist before proceeding
- Provide full paths to backup locations
- Confirm successful operations before marking complete
- Test restore procedures

## 🚨 EMERGENCY RECOVERY
If accidental data modification occurs:
1. STOP all operations immediately
2. Document exactly what happened
3. Check backup locations
4. Provide restore commands to user
5. Never attempt recovery without user approval

## 📋 OPERATION CHECKLIST
Before ANY file operation:
- [ ] Backup created and verified
- [ ] User permission obtained  
- [ ] Backup path provided to user
- [ ] Operation clearly explained
- [ ] Reversibility confirmed

---
**REMEMBER: User data is irreplaceable. When in doubt, DON'T.**