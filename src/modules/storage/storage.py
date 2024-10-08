import peewee as pw
from dataclasses import dataclass

db = pw.SqliteDatabase("new_db.db")
db.connect()


class BaseModel(pw.Model):
    class Meta:
        database = db


class Photo(BaseModel):
    id = pw.AutoField()
    nparray = pw.TextField()
    filename = pw.CharField(unique=True)


# @dataclass
# class Mask(BaseModel):
#     id = sa.Column(sa.Uuid, primary_key=True)
#     segmentation = sa.Column(sa.String)
#     area = sa.Column(sa.Float)
#     predicted_iou = sa.Column(sa.Float)
#     point_coords = sa.Column(sa.String)
#     stability_score = sa.Column(sa.Float)
#     crop_box = sa.Column(sa.String)
#     bbox = sa.Column(sa.String)
#     photo_id = sa.Column(sa.Uuid, sa.ForeignKey(Photo.id))
#     photo = sa.orm.relationship(Photo, backref="masks")

# Photo.truncate_table()
db.create_tables([Photo])

print("table:", Photo._meta.sorted_field_names)
print("photos:", [p.filename for p in Photo.select()])
