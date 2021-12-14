from django.db import models
from datetime import date
from django.utils import timezone

global SET_SIZE
SET_SIZE = 50

# Create your models here.
class VocabCard(models.Model):

    vocab_word = models.CharField(max_length=30)

    #defining parts of speech
    ADJECTIVE = 'Adjective'
    NOUN = 'Noun'
    VERB = 'Verb'
    PARTS_OF_SPEECH = [
        (ADJECTIVE,'Adjective'),
        (NOUN,'Noun'),
        (VERB,'Verb')
    ]
    vocab_pos = models.CharField(
    max_length = 10,
    choices = PARTS_OF_SPEECH,
    default = ADJECTIVE,
    )

    vocab_meaning = models.TextField()
    vocab_sentence = models.TextField(blank=True,null=True)
    vocab_synonyms = models.CharField(max_length=100,null=True,blank=True)
    
    bookmarked = models.BooleanField(default=False)
    re_learn = models.BooleanField(default=False)
    date_added = models.DateField(default=date.today,blank=True)
    set_number = models.IntegerField(default=0,blank=True)

    def __str__(self):

        return self.vocab_word

    def save(self,*args,**kwargs):
        is_new = self.pk is None
        
        if is_new:
            
            size = VocabCard.objects.all().count()
            
            if size==0:
                self.set_number = 1
            elif size%SET_SIZE==0:
                last = VocabCard.objects.last()
                self.set_number=last.set_number+1
            else:
                last = VocabCard.objects.last()
                self.set_number=last.set_number
            
        super(VocabCard,self).save(*args,**kwargs)

class TempDeck(models.Model):
    word_id = models.IntegerField()
        

class Streak(models.Model):
    date = models.DateField(default=date.today,blank=True)
    count = models.IntegerField(default=1)
    longest_streak = models.IntegerField(default=1)
