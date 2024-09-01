from django.core.management.base import BaseCommand

from News_app.models import Category, Post


class Command(BaseCommand):
    help = "Удаляет все посты в выбранной категории"
    requires_migrations_checks = True  # оповещение о наличии не примененных миграций

    def handle(self, *args, **options):

        def add_arguments(self, parser):
            parser.add_argument('category', type=str)

        ans = input('Do you really want to delete all posts in the category {options["category"]}? yes/no')

        if ans != 'yes':
            self.stdout.write(self.style.ERROR("Aborted"))
            return
        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS
                              ('Successfully deleted all posts in the category {options["category"]}'))
        except category.DoesNotExist:
            self.stdout.write(self.style.ERROR('Category {options["category"]} does not exist'))














