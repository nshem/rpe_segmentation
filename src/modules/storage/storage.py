import os
import shutil
import peewee as pw
from dataclasses import dataclass
import datetime


db = pw.SqliteDatabase("db.db")
db.connect()


class BaseModel(pw.Model):
    class Meta:
        database = db


class Photo(BaseModel):
    id = pw.AutoField()
    nparray = pw.TextField()
    filename = pw.CharField(unique=True)

    def has_masks(self):
        return Mask.select().where(Mask.photo_id == self.id).exists()

    def delete_masks(self):
        return Mask.delete().where(Mask.photo_id == self.id).execute()


class Mask(BaseModel):
    id = pw.AutoField()
    original_dict = pw.TextField()
    color = pw.TextField()
    batch_id = pw.DateTimeField()
    photo = pw.ForeignKeyField(Photo, backref="masks")
    photo_id = pw.FieldAccessor(Photo, "id", "photo_id")


db.create_tables([Photo, Mask])
n_imgs, n_masks = len(Photo.select()), len(Mask.select())
print(f"db: photos: {n_imgs}, masks: {n_masks}")

if os.path.exists("db.db") and (n_imgs > 0 or n_masks > 0):
    # Make a copy of db file in archive directory if it has data
    os.makedirs("archive", exist_ok=True)
    shutil.copy("db.db", os.path.join("archive", f"db_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.db"))

    # Truncate table
    Photo.truncate_table()
    Mask.truncate_table()

    print(f"Truncated db: photos: {len(Photo.select())}, masks: {len(Mask.select())}")
