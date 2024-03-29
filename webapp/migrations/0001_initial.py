# Generated by Django 2.0.3 on 2018-03-28 00:33

from django.db import migrations, models
import django.db.models.deletion
import webapp.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('tipo', models.CharField(blank=True, max_length=10, null=True)),
                ('file', models.FileField(upload_to=webapp.utils.UploadToPathAndRename('uploads/archivos'))),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ejemplo_De_Uso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('disciplinas', models.ManyToManyField(blank=True, related_name='ejemplos_de_uso', to='webapp.Disciplina')),
            ],
        ),
        migrations.CreateModel(
            name='Estrategia_Pedagogica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Herramienta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('tipo_de_licencia', models.CharField(blank=True, max_length=50, null=True)),
                ('sitio', models.URLField(blank=True, null=True)),
                ('descarga', models.URLField(blank=True, null=True)),
                ('restricciones_de_uso', models.TextField(blank=True, null=True)),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Informacion_Tecnica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion_funcional', models.TextField(blank=True, null=True)),
                ('sistemas_operativos', models.CharField(blank=True, max_length=255, null=True)),
                ('version', models.CharField(blank=True, max_length=10, null=True)),
                ('integracion_con_lms', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='herramienta',
            name='informacion_tecnica',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='herramienta', to='webapp.Informacion_Tecnica'),
        ),
        migrations.AddField(
            model_name='ejemplo_de_uso',
            name='estrategia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ejemplos_de_uso', to='webapp.Estrategia_Pedagogica'),
        ),
        migrations.AddField(
            model_name='ejemplo_de_uso',
            name='herramientas',
            field=models.ManyToManyField(blank=True, related_name='ejemplos_de_uso', to='webapp.Herramienta'),
        ),
        migrations.AddField(
            model_name='archivo',
            name='ejemplo_de_uso',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='archivos', to='webapp.Ejemplo_De_Uso'),
        ),
    ]
