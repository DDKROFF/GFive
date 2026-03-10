from django.contrib import admin
from django import forms
from .models import Hall, Device, Computer, Console

class DeviceAdminForm(forms.ModelForm):
    # Поля для компьютера
    cpu = forms.CharField(max_length=100, required=False, label="Процессор")
    gpu = forms.CharField(max_length=100, required=False, label="Видеокарта")
    ram_gb = forms.IntegerField(min_value=1, required=False, label="ОЗУ (ГБ)")
    storage_gb = forms.IntegerField(min_value=1, required=False, label="Накопитель (ГБ)")
    os = forms.CharField(max_length=100, required=False, label="ОС")
    has_webcam = forms.BooleanField(required=False, label="Веб-камера")
    has_microphone = forms.BooleanField(required=False, label="Микрофон")

    # Поля для консоли
    console_type = forms.ChoiceField(choices=Console.ConsoleType.choices, required=False, label="Тип консоли")
    controller_count = forms.IntegerField(min_value=1, max_value=8, required=False, label="Количество контроллеров")
    has_kinect = forms.BooleanField(required=False, label="Kinect/камера")
    has_vr_support = forms.BooleanField(required=False, label="Поддержка VR")
    console_storage_gb = forms.IntegerField(required=False, label="Объем накопителя (ГБ)")

    class Meta:
        model = Device
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # При редактировании подставляем значения из связанных моделей
        if self.instance and self.instance.pk:
            if hasattr(self.instance, 'computer_details'):
                comp = self.instance.computer_details
                self.fields['cpu'].initial = comp.cpu
                self.fields['gpu'].initial = comp.gpu
                self.fields['ram_gb'].initial = comp.ram_gb
                self.fields['storage_gb'].initial = comp.storage_gb
                self.fields['os'].initial = comp.os
                self.fields['has_webcam'].initial = comp.has_webcam
                self.fields['has_microphone'].initial = comp.has_microphone
            elif hasattr(self.instance, 'console_details'):
                cons = self.instance.console_details
                self.fields['console_type'].initial = cons.console_type
                self.fields['controller_count'].initial = cons.controller_count
                self.fields['has_kinect'].initial = cons.has_kinect
                self.fields['has_vr_support'].initial = cons.has_vr_support
                self.fields['console_storage_gb'].initial = cons.storage_gb

    def save(self, commit=True):
        device = super().save(commit=False)
        if commit:
            device.save()
        # Сохраняем или обновляем связанные объекты в зависимости от типа
        device_type = self.cleaned_data.get('device_type')
        if device_type == 'computer':
            Computer.objects.update_or_create(
                device=device,
                defaults={
                    'cpu': self.cleaned_data['cpu'],
                    'gpu': self.cleaned_data['gpu'],
                    'ram_gb': self.cleaned_data['ram_gb'],
                    'storage_gb': self.cleaned_data['storage_gb'],
                    'os': self.cleaned_data['os'],
                    'has_webcam': self.cleaned_data['has_webcam'],
                    'has_microphone': self.cleaned_data['has_microphone'],
                }
            )
            # Удаляем консоль, если она была
            Console.objects.filter(device=device).delete()
        elif device_type == 'console':
            Console.objects.update_or_create(
                device=device,
                defaults={
                    'console_type': self.cleaned_data['console_type'],
                    'controller_count': self.cleaned_data['controller_count'],
                    'has_kinect': self.cleaned_data['has_kinect'],
                    'has_vr_support': self.cleaned_data['has_vr_support'],
                    'storage_gb': self.cleaned_data['console_storage_gb'],
                }
            )
            Computer.objects.filter(device=device).delete()
        else:
            # Если тип не выбран — удаляем связанные объекты
            Computer.objects.filter(device=device).delete()
            Console.objects.filter(device=device).delete()
        return device

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_capacity', 'created_at')
    search_fields = ('name',)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    form = DeviceAdminForm
    list_display = ('inventory_number', 'device_type', 'status', 'hall')
    list_filter = ('device_type', 'status', 'hall')
    search_fields = ('inventory_number',)
    readonly_fields = ('inventory_number',)  # Запрещаем ручное редактирование
    fieldsets = (
        (None, {
            'fields': ('hall', 'device_type', 'status', 'inventory_number')
        }),
        ('Характеристики компьютера', {
            'classes': ('computer-fields',),
            'fields': ('cpu', 'gpu', 'ram_gb', 'storage_gb', 'os', 'has_webcam', 'has_microphone')
        }),
        ('Характеристики консоли', {
            'classes': ('console-fields',),
            'fields': ('console_type', 'controller_count', 'has_kinect', 'has_vr_support', 'console_storage_gb')
        }),
    )

    class Media:
        js = ('admin/js/device_admin.js',)  # Подключаем JS для переключения полей

@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ('device', 'cpu', 'ram_gb', 'storage_gb')
    raw_id_fields = ('device',)

@admin.register(Console)
class ConsoleAdmin(admin.ModelAdmin):
    list_display = ('device', 'console_type', 'controller_count')
    raw_id_fields = ('device',)