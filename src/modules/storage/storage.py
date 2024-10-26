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


# Photo.truncate_table()
# Mask.truncate_table()
db.create_tables([Photo, Mask])
print(f"db: photos: {len(Photo.select())}, masks: {len(Mask.select())}")
