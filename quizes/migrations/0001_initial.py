# Generated by Django 3.1.14 on 2022-02-08 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('number_of_questions', models.PositiveSmallIntegerField()),
                ('time_to_complete', models.PositiveIntegerField(help_text='How many time can your student complete your quiz?')),
                ('difficulty', models.CharField(choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard'), ('really hard', 'really hard')], max_length=12)),
                ('number_of_questions_to_pass', models.PositiveIntegerField(help_text='How many number of questions does student need to pass your quiz?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('attempts', models.PositiveSmallIntegerField(blank=True, default='1')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_author', to=settings.AUTH_USER_MODEL)),
                ('created_for', models.ManyToManyField(related_name='created_for', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizes',
            },
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('score', models.PositiveIntegerField(help_text='How can you rate your score?')),
                ('description', models.TextField(blank=True, max_length=10000)),
                ('attempt', models.PositiveSmallIntegerField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizes.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Results',
                'verbose_name_plural': 'Results',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=150)),
                ('type', models.CharField(choices=[('radio', 'radio'), ('text', 'text'), ('listbox', 'listbox')], default='radio', max_length=9)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizes.quiz')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Attempts',
            fields=[
                ('number', models.PositiveIntegerField()),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_attempts', to='quizes.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_attempts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Attempts',
                'verbose_name_plural': 'Attempts',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=150)),
                ('is_correct', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizes.question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizes.quiz')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
        ),
    ]
