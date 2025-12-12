# forms.py
from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full bg-gray-900 border border-gray-800 rounded-lg px-4 py-3 text-white font-mono focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-500 transition duration-200 placeholder-gray-600',
                'placeholder': 'Enter your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-gray-900 border border-gray-800 rounded-lg px-4 py-3 text-white font-mono focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-500 transition duration-200 placeholder-gray-600',
                'placeholder': 'your.email@example.com'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full bg-gray-900 border border-gray-800 rounded-lg px-4 py-3 text-white font-mono focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-500 transition duration-200 placeholder-gray-600 resize-none',
                'placeholder': 'Write your message here...',
                'rows': 5
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = ''