from django import forms
# from core.models import Invitees

class ProblemFilterForm(forms.Form):
    category = forms.ChoiceField(choices=(('None',None),('A','A'),('B','B'),('C','C'),('D','D'),('E','E'),('F','F'),('G','G'),('H','H')),required=False)
    ratingmin = forms.IntegerField(required=False)
    ratingmax = forms.IntegerField(required=False)
    tags = forms.CharField(max_length=100,required=False,help_text="Enter comma separated strings Ex: dp, math")
    show_tags = forms.BooleanField(required=False)

# class InviteForm(forms.ModelForm):
#     class Meta:
#         model = Invitees
#         exclude = ['status','currtime']
    