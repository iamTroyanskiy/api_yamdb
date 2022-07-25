# Generated by Django 2.2.16 on 2022-07-21 08:16

from django.db import migrations, models
import django.db.models.deletion
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220719_0815'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название жанра')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug жанра')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='Название')),
                ('year', models.IntegerField(validators=[reviews.validators.validate_year], verbose_name='Год выпуска')),
                ('description', models.TextField(max_length=200, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
            },
        ),
        migrations.RemoveField(
            model_name='titles',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='titles',
            name='genre',
        ),
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
        migrations.DeleteModel(
            name='Genres',
        ),
        migrations.DeleteModel(
            name='Titles',
        ),
        migrations.AddField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.Category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(related_name='titles', to='reviews.Genre', verbose_name='Жанр'),
        ),
    ]