from django.core.management.base import BaseCommand, CommandError
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
            questions.addquestions(options['inputfile'])
        else:
            questions.addquestions()

        self.stdout.write(self.style.SUCCESS('Successfully added questions'))