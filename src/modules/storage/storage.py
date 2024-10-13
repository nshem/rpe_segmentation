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


class Mask(BaseModel):
    id = pw.AutoField()
    original_dict = pw.TextField()
    color = pw.TextField()
    batch_id = pw.DateTimeField()
    photo = pw.ForeignKeyField(Photo, backref="masks")
    photo_id = pw.FieldAccessor(Photo, "id", "photo_id")

    def delete_batch(self, batch_id: datetime.datetime):
        self.delete().where(Mask.batch_id == batch_id)


# Photo.truncate_table()
# Mask.truncate_table()
db.create_tables([Photo, Mask])

print("photos table:", Photo._meta.sorted_field_names)
print("photos:", [p.filename for p in Photo.select()])
print("masks table:", Mask._meta.sorted_field_names)
print("masks:", [m.id for m in Mask.select()])
