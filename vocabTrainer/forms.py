from django.forms import ModelForm
from .models import VocabCard
from django import forms

class VocabCardForm(ModelForm):
    vocab_word = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder':'type your word',
            'class':'vocab-word-input input-vocab',
            'autofocus':'autofocus'
        }
    ),label='')

    choices = [('Adjective','Adjective'),
                ('Noun','Noun'),
                ('Verb','Verb')]

    vocab_pos = forms.ChoiceField(label="part of speech",choices=choices)

    vocab_meaning = forms.CharField(widget=forms.Textarea(
        attrs= {
            'placeholder':'type the meaning of the word',
            'class':'vocab-meaning-input'
        }
    ),label='')

    vocab_sentence = forms.CharField(widget=forms.Textarea(
        attrs= {
            'placeholder':'example sentence',
            'class':'vocab-sentence-input input-vocab'
        }
    ),label='',required=False)

    vocab_synonyms = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder':'synonyms',
            'class':'vocab-synonyms-input input-vocab',
            
        }
    ),label='',required=False)

    # bookmarked = forms.CharField(widget=forms.CheckboxInput())

    class Meta:
        model = VocabCard
        fields = ['vocab_word','vocab_pos','vocab_meaning','vocab_sentence','vocab_synonyms','bookmarked','re_learn','date_added','set_number']