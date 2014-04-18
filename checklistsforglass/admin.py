from django.contrib import admin
from models import Checklist, ChecklistV2, ChecklistElement, Device, UnregisteredDevice

admin.site.register(Checklist)
admin.site.register(ChecklistV2)
admin.site.register(ChecklistElement)
admin.site.register(Device)
admin.site.register(UnregisteredDevice)
