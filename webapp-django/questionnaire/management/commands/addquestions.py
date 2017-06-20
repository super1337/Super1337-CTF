from django.core.management.base import BaseCommand

from questionnaire.questions import questions


class Command(BaseCommand):
    help = 'Adds the questions from input JSON file to Database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--inputfile',
            dest='inputfile',
            help='Path of the input JSON file'
        )

    def handle(self, *args, **options):
        if options['inputfile']:
            ret = questions.addquestions(options['inputfile'])
        else:
            ret = questions.addquestions()

        self.stdout.write(self.style.SUCCESS('Successfully added questions to DB from \'{}\''.format(ret)))
