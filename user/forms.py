from django.forms import ModelForm
from django.forms import ValidationError

from user.models import Profile


class ProfileModelForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def clean_max_distance(self):
        data = self.clean()
        min_distance = data['min_distance']
        max_distance = data['max_distance']
        if min_distance >= max_distance:
            raise ValidationError('min_distance is greater than max_distance')
        return max_distance

    def clean_max_dating_age(self):
        data = self.clean()
        min_dating_age = data['min_dating_age']
        max_dating_age = data['max_dating_age']
        if min_dating_age >= max_dating_age:
            raise ValidationError('min_dating_age is greater than max_dating_age')
        return max_dating_age
