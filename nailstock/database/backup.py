import shutil
from datetime import datetime
from pathlib import Path

def crear_respaldo(ruta_destino=None):
    """Crea un respaldo de la base de datos"""
    db_path = Path("database/nailstack.db")
    
    if not db_path.exists():
        raise FileNotFoundError("La base de datos no existe")
    
    if ruta_destino is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_destino = f"backups/nailstack_backup_{timestamp}.db"
    
    Path(ruta_destino).parent.mkdir(parents=True, exist_ok=True)
    
    # Crear copia de la base de datos
    shutil.copy2(db_path, ruta_destino)
    
    return ruta_destino

def restaurar_respaldo(ruta_respaldo):
    """Restaura la base de datos desde un respaldo"""
    db_path = Path("database/nailstack.db")
    
    if not Path(ruta_respaldo).exists():
        raise FileNotFoundError("El archivo de respaldo no existe")
    
    # Hacer respaldo de la base actual antes de restaurar
    crear_respaldo(f"backups/pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
    
    # Restaurar desde respaldo
    shutil.copy2(ruta_respaldo, db_path)
    
    return True