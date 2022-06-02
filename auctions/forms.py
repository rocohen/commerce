from django import forms
from django.forms import TextInput, NumberInput, URLInput, Textarea, Select
from .models import Listing, Comment, Bid, Category

class ListingForm(forms.ModelForm):

  class Meta:
    model = Listing
    fields = ('title', 'imageURL', 'category', 'startingBid', 'description')
    labels = {
      'title': '* Title',
      'imageURL': 'Image URL',
      'category': '* Category',
      'startingBid': '* Starting Bid',
      'description': '* Description'
    }
    widgets = {
      'title': TextInput(attrs={'class': 'form-control mb-3'}),
      'imageURL': URLInput(attrs={'class': 'form-control mb-3'}),
      'category': Select(attrs={'class': 'form-control mb-3'}),
      'startingBid': NumberInput(attrs={'class': 'form-control mb-3'}),
      'description': Textarea(attrs={'class': 'form-control mb-3'})
    }

class CommentForm(forms.ModelForm):

  class Meta:
    model = Comment
    fields = ('content',)
    labels = {
      'content': 'Leave a comment',
    }
    widgets = {
      'content': Textarea(attrs={'class': 'form-control', 'rows': 4})
    }

class BidForm(forms.ModelForm):

  class Meta:
    model = Bid
    fields = ('amountBid',)
    labels = {
      'amountBid': ' ',
    }
    widgets = {
      'amountBid': NumberInput(attrs={'class': 'form-control mr-sm-2'})
    }