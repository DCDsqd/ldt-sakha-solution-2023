from sqlalchemy.orm import Session
from db_models import YtTable, VkTable, TgTable


def yt_save_data_to_db(db: Session, id_value: str, json_value: dict):
    # Создание нового объекта
    new_entry = YtTable(id=id_value, value=json_value)

    # Добавление объекта в сессию и сохранение его в базе данных
    db.add(new_entry)
    db.commit()


def yt_get_by_id(db: Session, record_id: str):
    record = db.query(YtTable).filter(YtTable.id == record_id).first()
    return record.value if record else None


def vk_save_data_to_db(db: Session, id_value: int, json_value: dict):
    # Создание нового объекта
    new_entry = VkTable(id=id_value, value=json_value)

    # Добавление объекта в сессию и сохранение его в базе данных
    db.add(new_entry)
    db.commit()


def vk_get_by_id(db: Session, record_id: int):
    record = db.query(VkTable).filter(VkTable.id == record_id).first()
    return record.value if record else None


def tg_save_data_to_db(db: Session, id_value: int, json_value: dict):
    # Создание нового объекта
    new_entry = TgTable(id=id_value, value=json_value)

    # Добавление объекта в сессию и сохранение его в базе данных
    db.add(new_entry)
    db.commit()


def tg_get_by_id(db: Session, record_id: int):
    record = db.query(TgTable).filter(TgTable.id == record_id).first()
    return record.value if record else None
