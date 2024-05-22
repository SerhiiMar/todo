from django import forms

from tasks.models import Tag, Task


class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": 'datetime-local',
            }
        )
    )

    class Meta:
        model = Task
        fields = ("title", "content", "deadline", "tags")
